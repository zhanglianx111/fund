#!/bin/bash
MYSQL_IMAGE="mysql:8.0"
MYSQL_NAME="mysql_fund"
MYSQL_PASSWORD="pw"
MYSQL_DATA_DIR=""

# check mysql data directory
## for mac
DATA_DIR="/Users/zhanglianxiang/go/src/github.com/zhanglianx111/fund/mysql_data"
ls ${DATA_DIR}
if [ $? -ne 0 ];then
	mkdir -p ${DATA_DIR}
fi
## for linux



# check to exist mysql container
info=`docker ps -a | grep ${MYSQL_NAME}`
# mysql container not exist
if [ "X${info}" == "X" ];then
	docker run -v ${DATA_DIR}:/var/lib/mysql --name ${MYSQL_NAME} -p 3306:3306 -p 33060:33060 -e MYSQL_ROOT_PASSWORD=${MYSQL_PASSWORD} -d ${MYSQL_IMAGE}
else
	# get running status for mysql container
	statusUP=`docker ps --filter status=running | grep ${MYSQL_NAME}`
	statusExited=`docker ps -a --filter status=exited | grep ${MYSQL_NAME}`
	statusPaused=`docker ps -a --filter status=paused | grep ${MYSQL_NAME}` 
	if [ "X${statusExited}" != "X" ];then
		docker start ${MYSQL_NAME}
		if [ $? -ne 0 ];then
			echo "start msyql container failed"
			exit 1
		fi
	elif [ "X${statusPaused}" != "X" ];then
		docker unpause ${MYSQL_NAME}
		if [ $? -ne 0 ];then
			echo "unpause msyql container failed"
			exit 2
		fi
	elif [ "X${statusUP}" != "X" ];then
		echo "mysql container is running"
	fi
fi