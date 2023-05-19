# SAR-CoV-2 Nucleocapsid-Cytokine Docking Analyses

<h3 align="right">Tuple, LLC and MIT Lincoln Labs</h3>

Large scale, _in silico_ interaction analyses of SARS-CoV-2 nucleocapsid protein variants against human cytokines.

## HPC Runs

### Docker
```bash
docker run -ti -v C:\Users\Colby\Documents\GitHub\SARS-CoV-2_N-Cytokine_Docking\cluster_tests:/inputs haddock2_4 /inputs/SARS-CoV-2_N_Wu1__CXCL12alpha/run-docking.csh /inputs/SARS-CoV-2_N_Wu1__CXCL12alpha

docker run -v C:\Users\Colby\Documents\GitHub\SARS-CoV-2_N-Cytokine_Docking\cluster_tests:/inputs --name haddock2_4_test1 -d haddock2_4
docker exec -it haddock2_4_test1 /bin/tcsh
```

### Singularity
```bash
singularity pull haddock.sif docker://cford38/haddock:2.4

cd submission
bash submist_dist.sh
```
