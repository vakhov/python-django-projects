#!/bin/bash

case "$1" in
"start")
python manage.py runfcgi method=prefork host=127.0.0.1 port=8801 pidfile=/tmp/mario-testing.pid
;;
"stop")
kill -9 `cat /tmp/mario-testing.pid`
;;
"restart")
$0 stop
sleep 1
$0 start
;;
*) echo "Usage: ./server.sh {start|stop|restart}";;
esac
