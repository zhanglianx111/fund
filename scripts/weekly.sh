table=$1
options=$2
if [ "X${options}" == "X" ];then
    echo "need options for grep command"
    exit 1
fi
today=`date +%m.%d` #星期几，例如：星期六 today=6
today0=`date -d -5day +%Y%m%d`

today1=`date -d -12day +%Y%m%d`

today2=`date -d -19day +%Y%m%d`

today3=`date -d -26day +%Y%m%d`

days_list=($today0 $today1 $today2 $today3)


function nextDayOfDay()
{
    start=$1
    days=$2
    startDay=`date +'%Y%m%d' -d ${start}`
    declare -i index
    index=0
    while [ ${index} -lt ${days} ]
    do
        date=`date -d "${startDay} ${index} days" +"%m.%d"`
        index=${index}+1
    done
    echo $date
}


for d in ${days_list[@]};
do
    friday=`nextDayOfDay ${d} 5`
    monday=`date +%m.%d -d ${d}`
    python fund.py rise_all_by_type -t ${table} -fd ${monday} -td ${friday} |grep -E ${options}
    echo "${monday} --> ${friday} --------------------------------------------------------------------------------------------------------------------------"
    echo 
done

python fund.py rise_all_by_type -t ${table} -fd ${monday} -td ${today} |grep -E ${options}
echo "${monday} --> ${today} --------------------------------------------------------------------------------------------------------------------------"
