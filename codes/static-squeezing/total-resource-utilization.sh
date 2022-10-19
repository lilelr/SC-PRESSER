#!/bin/bash

if [ $# != 3 ] ; then
echo "USAGE: $0 TABNAME"
echo " e.g.: $0 svd_large 300 0.1, the firt is workload name and the second is the duration in seconds, and the third is CPU_alpha"
exit 1;
fi

current_date_time=`date  '+%Y-%m-%d-%H-%M'`
echo "current_date_time is: $current_date_time"

workload_name=$1
duration=$2 # in seconds
cpu_alpha=$3 # in float
workload_name_with_time=$workload_name"-time-"$current_date_time

work_dir="/home/lemaker/open-source/Pressor/papers_data/"$workload_name"/"$workload_name_with_time"/"
leftover_programs_dir="/home/lemaker/open-source/Pressor/paper_codes/leftovers/"

if test -d $work_dir; then
    echo "work_dir has existed."
else
  mkdir -p $work_dir
fi

echo "start master first"
./docker-stats-memory-GB-master.sh $workload_name_with_time &
./local-start-docker-stats.sh $workload_name_with_time hadoop-slave6 &
./local-start-docker-stats.sh $workload_name_with_time hadoop-slave11 &

echo "start slaves"

# Options for SSH.
export SSH_OPTS="-f -o StrictHostKeyChecking=no -o ConnectTimeout=2"


# slavers_array=(01 02 03 04 05 08 09 10)

# Start slaves.


n=0
unset slaves
while read line; do
  slaves[$n]=$line
  ((n++))
done < "slaveList"


item='p09'
echo "Starting docker-stats  on ${item}"
echo ssh ${SSH_OPTS} lemaker@${item} ${daemon}
daemon="nohup /home/lemaker/scripts-chameleon/docker/local-start-docker-stats.sh $workload_name_with_time hadoop-slave1.1"
ssh ${SSH_OPTS} lemaker@${item} ${daemon}
daemon="nohup /home/lemaker/scripts-chameleon/docker/local-start-docker-stats.sh $workload_name_with_time hadoop-slave5"
ssh ${SSH_OPTS} lemaker@${item} ${daemon}
daemon="nohup /home/lemaker/scripts-chameleon/docker/local-start-docker-stats.sh $workload_name_with_time hadoop-slave10"
ssh ${SSH_OPTS} lemaker@${item} ${daemon}

item='p10'
echo "Starting docker-stats  on ${item}"
echo ssh ${SSH_OPTS} lemaker@${item} ${daemon}
daemon="nohup /home/lemaker/scripts-chameleon/docker/local-start-docker-stats.sh $workload_name_with_time hadoop-slave2"
ssh ${SSH_OPTS} lemaker@${item} ${daemon}
daemon="nohup /home/lemaker/scripts-chameleon/docker/local-start-docker-stats.sh $workload_name_with_time hadoop-slave4"
ssh ${SSH_OPTS} lemaker@${item} ${daemon}
daemon="nohup /home/lemaker/scripts-chameleon/docker/local-start-docker-stats.sh $workload_name_with_time hadoop-slave9"
ssh ${SSH_OPTS} lemaker@${item} ${daemon}

daemon="nohup /home/lemaker/scripts-chameleon/docker/local-start-docker-stats.sh $workload_name_with_time hadoop-slave12"
ssh ${SSH_OPTS} lemaker@${item} ${daemon}


item='p11'
echo "Starting docker-stats  on ${item}"
echo ssh ${SSH_OPTS} lemaker@${item} ${daemon}
daemon="nohup /home/lemaker/scripts-chameleon/docker/local-start-docker-stats.sh $workload_name_with_time hadoop-slave3"
ssh ${SSH_OPTS} lemaker@${item} ${daemon}

daemon="nohup /home/lemaker/scripts-chameleon/docker/local-start-docker-stats.sh $workload_name_with_time hadoop-slave7"
ssh ${SSH_OPTS} lemaker@${item} ${daemon}

# daemon="nohup /home/lemaker/scripts-chameleon/docker/local-start-docker-stats.sh $workload_name_with_time hadoop-slave8"
# ssh ${SSH_OPTS} lemaker@${item} ${daemon}

item='pc-2288H-V5'
echo "Starting docker-stats  on ${item}"
echo ssh ${SSH_OPTS} lemaker@${item} ${daemon}
daemon="nohup /home/lemaker/scripts-chameleon/docker/local-start-docker-stats.sh $workload_name_with_time hadoop-slave8"
ssh ${SSH_OPTS} lemaker@${item} ${daemon}

daemon="nohup /home/lemaker/scripts-chameleon/docker/local-start-docker-stats.sh $workload_name_with_time hadoop-slave13"
ssh ${SSH_OPTS} lemaker@${item} ${daemon}

# daemon="nohup /home/lemaker/scripts-chameleon/docker/local-start-docker-stats.sh $workload_name_with_time hadoop-slave8"
# ssh ${SSH_OPTS} lemaker@${item} ${daemon}

item='pc'
echo "Starting docker-stats  on ${item}"
echo ssh ${SSH_OPTS} lemaker@${item} ${daemon}
daemon="nohup /home/lemaker/scripts-chameleon/docker/local-start-docker-stats.sh $workload_name_with_time hadoop-slave9"
ssh ${SSH_OPTS} lemaker@${item} ${daemon}

daemon="nohup /home/lemaker/scripts-chameleon/docker/local-start-docker-stats.sh $workload_name_with_time hadoop-slave14"
ssh ${SSH_OPTS} lemaker@${item} ${daemon}

echo "sample the resource utilization for each docker container for ${duration} seconds"
sleep ${duration}
echo "execute the stop all docker stats command"
./stop-all-docker-stats.sh

# fetch dstats data from each node
fectchfiles="/home/lemaker/scripts-chameleon/docker/stats/"$workload_name_with_time"*"

fectchfile_on_slave4="/home/lemaker/scripts-chameleon/docker/stats/${workload_name_with_time}-hadoop*"
echo "fectchfiles are ${fectchfiles}"
cp  ${fectchfile_on_slave4} ${work_dir}
for item in ${slaves[*]}; do
  echo "fetching docker-stats  on ${item}"
  echo "scp lemaker@${item}:${fectchfiles} ${work_dir}"
  scp  lemaker@${item}:${fectchfiles} ${work_dir}
done

python3 ./avg_cpu_mem_per_second.py $workload_name $work_dir

echo "workload_name is $workload_name and workload_name_with_time is $workload_name_with_time"
echo "work_dir is $work_dir"

# /home/lemaker/open-source/Pressor/paper_codes/leftovers
# leftover_program="pandas_cpu_leftovers_6files_${workload_name}_large.py"
# fixed

wait # Wait for all the ssh's to finish.

