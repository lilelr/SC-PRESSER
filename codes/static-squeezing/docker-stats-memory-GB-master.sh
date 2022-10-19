#!/bin/bash
echo "lele begin"
## $1 -> workload_name $2-> docker_name


location=$(cd "$(dirname "$0")";pwd)
stats_dir=${location}/stats
if [ ! -f "$stats_dir" ];then
  mkdir "$stats_dir"
fi

stats_data=$1'-'$2'-'$(date +%Y-%m-%d_%H:%M:%S).csv


stats_data=$1'-'${HOSTNAME}'-'$(date +%Y-%m-%d_%H:%M:%S).csv

destination=${stats_dir}/${stats_data}

while true;
 do
  docker stats --no-stream | grep master | awk -F" " -v OFS=, -v date="$(date +%T)" '{ if(index($4, "MiB")) {gsub("MiB","",$4); print $4 / 1000} else {gsub("GiB","",$4); print date,$1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13,$14}}' >> ${destination};
  echo "lele add one";
 done
