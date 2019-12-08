#!/usr/bin/env bash
for i in `ps -ef|grep hzjm.wsgi|grep -v grep|awk '{print $2}'`
do
kill -9 $i
done
