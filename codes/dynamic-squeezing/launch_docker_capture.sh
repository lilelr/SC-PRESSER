#!/bin/bash

# "please input the primary_docker_name, secondary_docker_name, cpu_lower_bound, cpu_upper_bound, update_cpus"
# "cpu_lower_bound makes sense, the other two metrics do not work"
python3 docker_capture.py hadoop-slave6.1.jyquyq8eoldtbvk9z2h8twuih hadoop-slave11.1.du3x6odbxchwtbh4v213we7ds 10 40 30