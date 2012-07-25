#!/bin/bash

case "$1" in
"start")
python manage.py runfcgi method=prefork host=127.0.0.1 port=8883 pidfile=/tmp/brick.pid
;;
"stop")
kill -9 `cat /tmp/brick.pid`
;;
"restart")
$0 stop
sleep 1
$0 start
;;
*) echo "Usage: ./server.sh {start|stop|restart}";;
esac
