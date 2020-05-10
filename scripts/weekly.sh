#!/bin/bash
##############################################
# ./scripts/weekly.sh table-name weeks options
##############################################

function nextDayOfDay()
{
    start=$1
    days=$2

    startDay=`date +'%Y%m%d' -d ${start}`
    date=`date -d "${startDay} ${days} days" +"%Y%m%d"`
    echo $date
}

table=$1
weeks=`expr $2 - 1`
options=$3
#if [ "X${options}" == "X" ];then
#    echo "need options for grep command"
#    exit 1
#fi

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
days_list=()
for i in $(seq 0 ${weeks});do
    step=`expr -7 \* $i`
    days_list[i]=`nextDayOfDay ${today0} ${step}`
done

# 时间由远到近

for d in ${days_list[@]};
do
    friday_tmp=`nextDayOfDay ${d} 4`
    friday=`date +%m.%d -d ${friday_tmp}`
    monday=`date +%m.%d -d ${d}`
    echo "${monday} --> ${friday} -----------------------------------------------------------------------------------------------------------------------------------------------"
    if [ "X${options}" == "X" ];then
        python fund.py rise_all_by_type -t ${table} -fd ${monday} -td ${friday}
    else
        python fund.py rise_all_by_type -t ${table} -fd ${monday} -td ${friday} |grep -E ${options}
    fi
    echo
done

friday_tmp=`nextDayOfDay ${days_list[0]} 4`
friday=`date +%m.%d -d ${friday_tmp}`
if [ ${weeks} != 0 ];then
    echo "${monday} --> ${friday} -----------------------------------------------------------------------------------------------------------------------------------------------"
    if [ "X${options}" == "X" ];then
        python fund.py rise_all_by_type -t ${table} -fd ${monday} -td ${friday}
    else
        python fund.py rise_all_by_type -t ${table} -fd ${monday} -td ${friday} |grep -E ${options}
    fi
fi
