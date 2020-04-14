#! /bin/bash

# 昨天日期，此脚本执行的时间是获取上一天的基金净值，所有要获取昨天的日期
os=`uname`
yestoday=$1
if [ "X$yestoday" == "X" ];then
    if [ $os == "Linux" ];then
        echo $os > test.log
        echo `date` >> test.log
        yestoday=`date -d last-day +%m.%d`
    elif [ $os == "Darwin" ];then
        echo $os >> test.log
        echo `date` >> test.log
        yestoday=`date -v-1d +"%m.%d"`
    fi
fi

python fund.py routine -d ${yestoday}
