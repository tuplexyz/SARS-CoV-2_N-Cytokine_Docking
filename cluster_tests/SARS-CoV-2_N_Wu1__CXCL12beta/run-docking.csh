
#!/bin/csh
#
source $HOME/haddock/haddock2.4-2021-01/haddock_configure.csh
echo "====================================================================="
echo "====================================================================="
echo " RUNNING: SARS-CoV-2_N_Wu1__CXCL12beta PROTEIN-PROTEIN DOCKING "
echo "====================================================================="
echo "====================================================================="
haddock2.4 >&/dev/null
cd run1
patch -p0 -i ../run.cns.patch >&/dev/null
haddock2.4 >&haddock.out
cd ..
./ana_scripts/run_all.csh run1 >&/dev/null
../results-stats.csh run1
echo "====================================================================="
echo "====================================================================="
echo " DONE: SARS-CoV-2_N_Wu1__CXCL12beta PROTEIN-PROTEIN DOCKING COMPLETED  "
echo "====================================================================="
echo "====================================================================="
