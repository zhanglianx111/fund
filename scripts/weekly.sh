#!/bin/bash
function nextDayOfDay()
{
    start=$1
    days=$2

    startDay=`date +'%Y%m%d' -d ${start}`
    date=`date -d "${startDay} ${days} days" +"%Y%m%d"`
    echo $date
}

table=$1
options=$2
if [ "X${options}" == "X" ];then
    echo "need options for grep command"
    exit 1
fi

today=`date +%m.%d`   #今天日期
weekday=`date +%w`    # 星期几，例如：星期六 weekday=6; 星期日 weekday=0
# 如果今天是周一到周五, 本周不做计算
if [ ${weekday} -ge 1 -a ${weekday} -le 5 ];then
    offset=$(expr 6 + ${weekday})
elif [ ${weekday} == '6' ];then # 今天是周六
    offset=5

else # 今天是周日
    offset=6
fi

today0=`date -d -${offset}days +%Y%m%d`

monday0=`nextDayOfDay ${today0} 0`
monday1=`nextDayOfDay ${today0} -7`
monday2=`nextDayOfDay ${today0} -14`
monday3=`nextDayOfDay ${today0} -21`
# 时间由远到近
days_list=($monday3 $monday2 $monday1 $monday0)

for d in ${days_list[@]};
do
    friday_tmp=`nextDayOfDay ${d} 4`
    friday=`date +%m.%d -d ${friday_tmp}`
    monday=`date +%m.%d -d ${d}`
    echo "${monday} --> ${friday} -----------------------------------------------------------------------------------------------------------------------------------------------"
    python fund.py rise_all_by_type -t ${table} -fd ${monday} -td ${friday} |grep -E ${options}
    echo
done

monday=`date +%m.%d -d ${monday3}`
    echo "${monday} --> ${friday} -----------------------------------------------------------------------------------------------------------------------------------------------"
python fund.py rise_all_by_type -t ${table} -fd ${monday} -td ${friday} |grep -E ${options}
