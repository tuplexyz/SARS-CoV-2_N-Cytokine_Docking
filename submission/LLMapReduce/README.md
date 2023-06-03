
### Example LLMapReduce using Mapper and Input  
First steps:  
Go to your experiment directory such as `N_cytokine_docking/cluster_tests/`  
Make an input filelist:
`ls > experiment.list`  
Edit the experiment.list and remove the last line (ls will list the experiment.list file itself in the file)  

On the SuperCloud run the following command:  
`LLMapReduce --mapper=haddock_mapper.sh --input=experiment.list --output=results --keep=true --cpuType=xeon-p8 --np=[2,2,24]`  

### LLMapReduce Explanation  
[First, Second, Third]:  
First - Number of compute nodes, also equivalent to number of slurm jobs (and JOBIDs).  
Second - Number of processes per node.  
Third - Number of threads per process.  

**Example `--np=[2,2,24]`**  
In this case say we have **4 experiments** we need to run, we need a total of **4 processes**.  
One submission of LLMapReduce results in one ARRAY_JOB.  

Rules:  
First x Second <= number of experiments.  
Second x Third = number of physical cores on the compute node. (ie. 48 for xeon-p8)

2 = compute nodes / slurm jobs  
2 = 2 processes per node  
2 * 24 = 48 cores per node

Example format:  
ARRAY_JOB = 22945675  
JOBID = 22945675_1 and 22945675_2  

### Debugging and Logging  

The `--keep-true` flag above keeps the MAPRED folder in the format of MAPRED.#####  
The number in the directory name is random, but you can check the ARRAY_JOB it came from:
`cat MAPRED.#####/MapJOBID`  

You can also see the stdout for each process.  
The number of sub-directories corresponds to the number of JOBIDs.  
For example one JOBID for processes 0 and 1, on compute node d-19-11-3: 
```  
MAPRED.21818/logs/p0-p1_d-19-11-3/llmap.log-0  
MAPRED.21818/logs/p0-p1_d-19-11-3/llmap.log-1  
```  
and another subdir for JOBID#2 for processes 2 and 3, on compute node d-19-5-4:  
```  
MAPRED.21818/logs/p2-p3_d-19-5-4/llmap.log-2  
MAPRED.21818/logs/p2-p3_d-19-5-4/llmap.log-3  
``` 
