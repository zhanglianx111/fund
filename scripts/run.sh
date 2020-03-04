#!/bin/bash

# 定时执行任务脚本，脚本每天执行
# 工作内容：
#	1. 获取当天所有基金涨跌情况并排序 ✅
#	2. 统计当天涨跌基金个数，并发邮件 
#	3. 统计当天涨幅前100名，并发邮件
#	4. 统计当天平均涨幅，平均跌幅，并发邮件


# 昨天日期，此脚本执行的时间是获取上一天的基金净值，所有要获取昨天的日期
os=`uname`
yestoday=""
if [ $os == "Linux" ];then
	yestoday=`date -d last-day +%Y-%m-%d`
elif [ $os == "Darwin" ];then
	yestoday=`date -v-1d +"%Y-%m-%d"`
fi

python fund.py fetchall -d ${yestoday}
if [ $? -ne 0 ];then
	echo "error code:" $?
	echo "fetch all funds failed for" ${yestoday}
	exit 1
fi

python fund.py topn -d ${yestoday}
if [ $? -ne 0 ];then
	echo "error code:" $?
	echo "sort all funds failed for" ${yestoday}
	exit 2
fi
exit 0
