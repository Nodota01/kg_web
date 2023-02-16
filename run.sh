#!/bin/bash
#用jobs -l查看进程
#用kill %1杀掉进程
#用tail -f my.log查看日志
# nohup flask --app kgweb --debug run --host=0.0.0.0 --port=9999 > my.log 2>&1 & 
flask --app kgweb --debug run --host=0.0.0.0 --port=9999