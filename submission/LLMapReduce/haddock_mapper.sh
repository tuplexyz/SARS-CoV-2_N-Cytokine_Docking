#!/bin/bash
# HADDOCK Mapper Script for LLMapReduce (MIT SuperCloud)
#
#     Args:
#        $1 (str): relative path to experiment (e.g. SARS-CoV-2_N_Wu1__CXCL12beta/ )
#        dbwrite (TYPE, optional): DESCRIPTION. Defaults to False.
#
#    Returns:
#        Outputs from HADDOCK will appear in the run1 folder under the corresponding experiment.
#

# Set the relative or full path to the haddock SIF as needed here.
SIF=haddock.sif
# Set the experiment directory
EXP_DIR=N_cytokine_docking/cluster_tests/
# Generally you shouldn't need to change these.
export TMP=/state/partition1/user/seqer
export TMPDIR=/state/partition1/user/seqer

# Check the TMP defined above exists, if not create and chgrp.
if [ ! -d "$TMP" ]; then
  mkdir -p $TMP && chgrp -R seqer $TMP
fi

singularity run -B $EXP_DIR:/experiments,$TMP:$TMP $SIF /experiments/$1/run-docking.csh /experiments/$1