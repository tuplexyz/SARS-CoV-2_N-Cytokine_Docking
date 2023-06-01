# SARS-CoV-2 Nucleocapsid-Cytokine Docking Analyses

<h3 align="right">Tuple, LLC and MIT Lincoln Labs</h3>

Large scale, _in silico_ interaction analyses of SARS-CoV-2 nucleocapsid protein variants against human cytokines.

## HPC Runs

### Local Docker
```bash
## Run from `docker run` command
docker run -ti -v C:\Users\Colby\Documents\GitHub\SARS-CoV-2_N-Cytokine_Docking\cluster_tests:/inputs haddock2_4 /inputs/SARS-CoV-2_N_Wu1__CXCL12alpha/run-docking.csh /inputs/SARS-CoV-2_N_Wu1__CXCL12alpha

## Run interactively in the container's terminal
docker run -v C:\Users\Colby\Documents\GitHub\SARS-CoV-2_N-Cytokine_Docking\cluster_tests:/inputs --name haddock2_4_test1 -d haddock2_4
docker exec -it haddock2_4_test1 /bin/tcsh
```

### Singularity
```bash
singularity pull haddock.sif docker://cford38/haddock:2.4

cd submission
bash submit_dist.sh
```

### MIT SuperCloud Tests  
The SuperCloud automatically sets two env vars which interfere with HADDOCK. 
```
env |grep TMP
TMP=/state/partition1/slurm_tmp/22930272.0.0
TMPDIR=/state/partition1/slurm_tmp/22930272.0.
```
This results in errors like this because slurm_tmp is not user-writable.  
`/state/partition1/slurm_tmp/22929006.0.0/sh.vbg0Ln: No such file or directory.`  

After requesting an interactive node, you want to overwrite these.  
See here:  

```bash
LLsub -i -N 1
export TMP=/state/partition1/user/seqer
export TMPDIR=/state/partition1/user/seqer
```
Note: make sure that /state/partition1/user/seqer is created and has a group ownership of seqer. If not, run this from anywhere:  
```bash
mkdir /state/partition1/user/seqer
chgrp -R seqer /state/partition1/user/seqer
```

Now, make sure the state partition is bound inside the container:  
```bash
singularity run -B N_cytokine_docking/cluster_tests/:/experiments,/state/partition1/user/seqer:/state/partition1/user/seqer haddock.sif /experiments/SARS-CoV-2_N_Wu1__CXCL12beta/run-docking.csh /experiments/SARS-CoV-2_N_Wu1__CXCL12beta/
```
Also note, the default time limit of 30 min for interactive sessions is not enough for HADDOCK to finish.  
We need to put these into a mapper script (and possibly reducer script to cleanup the run files.

### UNCC HPC Tests
```bash
singularity exec haddock.sif /root/haddock/haddock2.4-2021-01/examples/protein-protein/run-example.csh

singularity run -B cluster_tests/:/experiments haddock.sif /experiments/SARS-CoV-2_N_Wu1__CXCL12beta/run-docking.csh /experiments/SARS-CoV-2_N_Wu1__CXCL12beta/
```




