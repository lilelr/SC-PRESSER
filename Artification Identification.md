
%START_LATEX

Artifact Check-List (Meta-Information)
• Program: PRESSER
Data set: TPC-DS queries
Software Dependencies: Ubuntu 20.04, Docker 20, Docker swarm, Spark 3.3.0, OpenJDK 8,  Python 3
Hardware Dependencies: A cluster consisting of six x86 physical servers. Each physical server is equipped with 48 Intel(R) Xeon(R) Silver CPU 4214 2.20 GHz cores and 128 GB DDR4 memory
Experiments: Running the TPC-DS queries on the cluster managed by PRESSER
How much time is needed to prepare workflow? 1 hours
How much time is needed to complete experiments
(approximately)? 1 hours
Publicly available? Yes
Github Link: https://github.com/lilelr/SC-PRESSER



## About PRESSER

The the  software architecture of PRESSER can be seen in our paper or via https://github.com/lilelr/SC-PRESSER.

PRESSER is a hybrid static dynamic mechanism atop Hadoop YARN to squeeze unused resources (i.e. CPU cores and memory) from Machine Learning Optimized Apach Spark (MLOS) and Dynamic Resource Allocation (DRAOS) applications by historical observations. The static mechanism called GAP squeezes the "gap amount" of resoruces between a MLOS or DRAOS application's peak used and allocated resource amount based on its last execution before it starts tis next execution. The dynamic mechanism, called $\alpha-CAP$ monitors the resource usages of a MLOS or DRAOS application durign its execution per second and dynamically squeezes the "gap amount" of resources between  $\alpha$ percentile of allocated resources and its acutally used ones. The squeezed resources from GAP and  $\alpha-CAP$ can be reprovisioned to other co-located applications to improve cluster resource utilziation and system throughput. 

Since PRESSER has two main techniques: GAP of static squeezing and $\alpha-CAP$ of dynamical squeezing. We provides two software artifacts. The first is the static squeezing (i.e, GAG) technique written in python and Linux shell. The Linux shell scripts in the folder "static-squeezing" are used to monitor and store the resource time series of each MLOS or DRAOS query running in our cluster. After collecting these resource time  series, we leverage the python scripts in the folder "squeezed-resource-MLOS_100G" or "squeezed-resource-MLOS_500G" to perform the GAP technique to squeeze up the the over-provisioned resources before execution for each MLOS or DRAOS query. For instance, the ""squeezed-resource-MLOS_500G/presser-dac-500G-6-containers-q15.ipynb" is used to do the static resource squeezing for the MLOS query Q15. 

The second artifact is about the $\alpha-CAP$ of dynamical squeezing, which is placed in the folder "dynamic-squeezing" and is implemented in python and Linux shell. To be specific, "dynamical squeezing/docker_capture.py" is used to control the resource limit (CPU cores or memory) of the co-located applications.  If the current used resource amount of the MLOS or DRAOS application is lower than the  $\alpha-percentile$ of the allocated one, then the difference between them would be transfered to the the co-located applation by  "dynamical squeezing/docker_capture.py".


## Github Link
https://github.com/lilelr/SC-PRESSER


## Basic Usage

Take MLOS applications as an example, but the usage for DRAOS applications is similar. 
Our experimental cluster is a docker cluster based on 6 physical servers. In total, we launch 12 Docker containers.  We divide the 12 Docker containers into 3 regions. The first region with 6 Docker containers is to run the MLOS applications. The second region with 3 Docker containers leverages the statically squeezed resources from the MLOS applications in the first region to run  non-MLOS applications randomly. And the third region also contains 3 Docker containers and reallocates the dynamically squeezed resources from MLOS applications to co-located applications. Each region deploys Hadoop 3.3 as the software infrastructure. The Spark framework employs Hadoop YARN as the underlying resource manager.


PRESSER leverages the docker command "**docker stats**" to record the resource usages of each MLOS application in GAP mechanism. And $\alpha-CAP$ mechanism employs the docker command  "**docker update**" to limit the available CPU and memory resources of a Docker container. By dynamically limiting the CPU and memory resources of a container where a non-MLOS application runs, $\alpha-CAP$ achieves the objective of squeezing CPU and memory resources from Docker containers running MLOS applications to Docker containers executing non-MLOS applications. 


%STOP_LATEX