
%START_LATEX

\section{Prerequisites}
TPC-DS v3, Docker 20, Docker swarm, Spark 3.3.0, Hadoop 3, Ubuntu 20.04.2, OpenJDK 8,  Python 3, Anaconda 3, pandas


\section{Basic Usage}

Take MLOS applications as an example, but the usage for DRAOS applications is similar. 
Our experimental cluster is a docker cluster based on 6 physical servers. In total, we launch 12 Docker containers.  We divide the 12 Docker containers into 3 regions. The first region with 6 Docker containers is to run the MLOS applications. The second region with 3 Docker containers leverages the statically squeezed resources from the MLOS applications in the first region to run  non-MLOS applications randomly. And the third region also contains 3 Docker containers and reallocates the dynamically squeezed resources from MLOS applications to co-located applications. Each region deploys Hadoop 3.3 as the software infrastructure. The Spark framework employs Hadoop YARN as the underlying resource manager.



\section{Installation}

Please see https://github.com/lilelr/SC-PRESSER.


\section{Data Sets Preparation}

We leverage the Spark version of TPC-DS and the installation of it is as follows:
https://github.com/lilelr/BaBench

\section{Experiment Steps}

Take MLOS applications as an example, but the usage for DRAOS applications is similar. 
Our experimental cluster is a docker cluster based on 6 physical servers  with 128 GB RAM and 48 CPU cores each. In total, we launch 12 Docker containers.  We divide the 12 Docker containers into 3 regions. The first region with 6 Docker containers is to run the MLOS applications. The second region with 3 Docker containers leverages the statically squeezed resources from the MLOS applications in the first region to run  non-MLOS applications randomly. And the third region also contains 3 Docker containers and reallocates the dynamically squeezed resources from MLOS applications to co-located applications. Each region deploys Hadoop 3.3 as the software infrastructure. The Spark framework employs Hadoop YARN as the underlying resource manager.

To see more details of environment setup, please see Please see https://github.com/lilelr/SC-PRESSER/README.md

1. When a user submits a MLOS TPC-DS query to the cluster, the script "static-squeezing/total-resource-utizliation.sh" is used to minitor the resource usages the cluster. We use the MLOS TPC-DS Q15 with the input data of 500GB for example. 

2. Upon the execution completion of Q15, we can run it again. But this time, we colocate second application (e.g., Q16) on the second region to harness the static squeezed resoures from Q15.

3. Simultaneously, the script \textbf{dynamic-squeezing/launch\_docker\_capture.sh} is luanched on the third region in order to reprovision the squeezed rsources from Q15 to run Q17.

4. For many MLOS applications co-running in the cluster, the \textbf{resource\_utilization/presser-ten-workloads-500G-0928-14-containers-sig-presser-static-dy-10minutes.ipynb} exhibits the comparison of resource utilization with and without PRESSER, which contains the Figures 18 and 19 in our paper. 

PRESSER leverages the docker command \textbf{docker stats} to record the resource usages of each MLOS application in GAP mechanism. And $\alpha-CAP$ mechanism employs the docker command  \textbf{docker update} to limit the available CPU and memory resources of a Docker container. By dynamically limiting the CPU and memory resources of a container where a non-MLOS application runs, $\alpha-CAP$ achieves the objective of squeezing CPU and memory resources from Docker containers running MLOS applications to Docker containers executing non-MLOS applications. 

\section{The estimation of the execution time to execute the experiment workflow}

Using the input data of 100 and 500 GB for evaluation, the average execution time for all 103 TPC-DS MLOS or DRAOS queries is below 120 seconds. Therefore, the estimated execution time to execute the experiment worklow is aboult 120 seconds for each MLOS or DRAOS appplication. 

\section{A complete description of the expected results and an evaluation of them}

We provide the exeperimental resutls of resource efficiency from a number of MLOS applications in the folder \textbf{squeezed-resources-MLOS\_100G} and \textbf{squeezed-resources-MLOS\_500G} with input data of 100 and 500 GB, respectively. 

PRESSER can leverage the squeezed resources from the MLOS or DRAOS applications to execute more co-located applications. In our experimental cluster, PRESSER can double the cluster throughput compared with the original cluster. That is, the original cluster could only run 103 queries in the cluster while PRSSER could run 206 queries at the same time without significantly hurting the performance of them. 

With input data of 100 GB, PRESSER can therefore save 22 
CPU cores and 17 GB memory on average per query in TPC-DS. As for 500 GB, PRESSER can save 63 CPU cores and 60 GB memory on average per query. We evaluate PRESSER on a 6-node Spark cluster by using103 Spark SQL queries from TPC-DS. The experimental
results show that PRESSER can improve CPU and memory utilization by 31\% and 20\% on average.

\section{How the expected results from the experiment workflow relate to the results found in the article}

The difference depends the number of physical serivers used for evalutaion. In the article, we use 6 physical servers. But the amount of squeezed resources would be more if you use more than 6 physical servers and thus the resource efficiency is improved more significantly. 


%STOP_LATEX
