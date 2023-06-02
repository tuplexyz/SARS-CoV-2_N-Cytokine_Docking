
### Example LLMapReduce using Mapper and Input  
First steps:  
Go to your experiment directory such as `N_cytokine_docking/cluster_tests/`  
Make an input filelist:
`ls > experiment.list`  
Edit the experiment.list and remove the last line (ls will list the experiment.list file itself in the file)  

On the SuperCloud run the following command:  
`LLMapReduce --mapper=haddock_mapper.sh --input=N_cytokine_docking/cluster_tests/ --output=results --keep=true --cpuType=xeon-p8 --np=[1,4,12]`  

Triples mode explanation [1,4,12]:  
1 = node / slurm task  
4 = 4 processes/jobs per node  
1 * 4 * 12 = 48 CPUs (max for the xeon-p8 node)  