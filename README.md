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

```bash
## MIT SuperCloud Tests
LLsub -i -N 1

singularity exec haddock.sif seqer_shared/N_cytokine_docking/cluster_tests/SARS-CoV-2_N_Wu1__CXCL12beta/run-docking.csh

singularity run -B N_cytokine_docking/cluster_tests/:/experiments haddock.sif /experiments/SARS-CoV-2_N_Wu1__CXCL12beta/run-docking.csh /experiments/SARS-CoV-2_N_Wu1__CXCL12beta/

singularity run -B N_cytokine_docking/cluster_tests/:/inputs haddock.sif /root/haddock/haddock2.4-2021-01/examples/protein-protein/run-example.csh

## UNCC HPC Tests
singularity exec haddock.sif /root/haddock/haddock2.4-2021-01/examples/protein-protein/run-example.csh

singularity run -B cluster_tests/:/experiments haddock.sif /experiments/SARS-CoV-2_N_Wu1__CXCL12beta/run-docking.csh /experiments/SARS-CoV-2_N_Wu1__CXCL12beta/
```




