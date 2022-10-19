#!/bin/bash
cd /home/lemaker/scripts-chameleon/docker/
## $1 -> workload_name_with_time $2-> docker_name
# e.g. svd_large-time-2022-6-1-12-9 hadoop-slave4
./docker-stats-memory-GB.sh $1 $2
