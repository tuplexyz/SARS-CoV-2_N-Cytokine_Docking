#!/bin/bash
#SBATCH --job-name=cford_haddock_dist
#SBATCH --partition=Orion
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=36
#SBATCH --constraint=skylake
#SBATCH --mem=300gb
#SBATCH --time=5:00:00

export SINGULARITY_CONTAINER_HOME=/home/gridsan/$USER/seqer_shared/N_cytokine_docking
# export SINGULARITY_TMPDIR=/scratch/$USER/tmp

export HOME=esm/model_weights
export PYTHONPATH=$PYTHONPATH:$SINGULARITY_CONTAINER_HOME/esm

export input_csv=data/HADDOCK_Results.csv

# module load singularity
singularity run $SINGULARITY_CONTAINER_HOME/haddock.sif

while IFS="," read -r complex_id experiment_path
do
  echo "Complex ID: $complex_id"
  echo "Protein Complex Path: $experiment_path"
  echo ""

  JOBID=$(sbatch --parsable submit_iter.sh $complex_id $protein_path)

done < <(tail -n +2 $input_csv)
