#!/bin/bash

sudo kill -9 `ps -ef|grep "docker-stats-memory-GB" |grep -v grep|awk '{print $2}'`

