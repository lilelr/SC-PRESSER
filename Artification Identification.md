%START_LATEX


\section{Artifact Check-List}


\begin{enumerate}
\item Program: PRESSER

\item Data Set: TPC-DS queries with 100 and 500 GB

\item Software Dependencies: Ubuntu 20.04, Docker 20, Docker swarm, Spark 3.3.0, OpenJDK 8,  Python 3

\item Hardware Dependencies: A cluster consisting of six x86 physical servers. Each physical server is equipped with 48 Intel(R) Xeon(R) Silver CPU 4214 2.20 GHz cores and 128 GB DDR4 memory

\item Experiments: Running the TPC-DS queries on the cluster managed by PRESSER

\item How much time is needed to prepare workflow? 1 hours

\item How much time is needed to complete experiments (approximately)? 1 hours

\item Publicly available? Yes Github Link: https://github.com/lilelr/SC-PRESSER
\end{enumerate}


\section{About PRESSER}


The the  software architecture of PRESSER can be seen in our paper or via https://github.com/lilelr/SC-PRESSER.


PRESSER is a hybrid static dynamic mechanism atop Hadoop YARN to squeeze unused resources (i.e. CPU cores and memory) from Machine Learning Optimized Apach Spark (MLOS) and Dynamic Resource Allocation (DRAOS) applications by historical observations. The static mechanism called GAP squeezes the "gap amount" of resoruces between a MLOS or DRAOS application's peak used and allocated resource amount based on its last execution before it starts tis next execution. The dynamic mechanism, called $\alpha-CAP$ monitors the resource usages of a MLOS or DRAOS application durign its execution per second and dynamically squeezes the "gap amount" of resources between  $\alpha$ percentile of allocated resources and its acutally used ones. The squeezed resources from GAP and  $\alpha-CAP$ can be reprovisioned to other co-located applications to improve cluster resource utilziation and system throughput. 

Since PRESSER has two main techniques: GAP of static squeezing and $\alpha-CAP$ of dynamical squeezing. We provides two software artifacts. The first is the static squeezing (i.e, GAG) technique written in python and Linux shell. The Linux shell scripts in the folder \textbf{static-squeezing} are used to monitor and store the resource time series of each MLOS or DRAOS query running in our cluster. After collecting these resource time  series, we leverage the python scripts in the folder \textbf{squeezed-resource-MLOS\_100G} or \textbf{squeezed-resource-MLOS\_500G} to perform the GAP technique to squeeze up the the over-provisioned resources before execution for each MLOS or DRAOS query. For instance, the \textbf{squeezed-resource-MLOS\_500G/presser-dac-500G-6-containers-q15.ipynb} is used to do the static resource squeezing for the MLOS query Q15. 

The second artifact is about the $\alpha-CAP$ of dynamical squeezing, which is placed in the folder \textbf{dynamic-squeezing} and is implemented in python and Linux shell. To be specific, \textbf{dynamical squeezing/docker\_capture.py} is used to control the resource limit (CPU cores or memory) of the co-located applications.  If the current used resource amount of the MLOS or DRAOS application is lower than the  $\alpha-percentile$ of the allocated one, then the difference between them would be transfered to the the co-located applation by this script.




%STOP_LATEX
