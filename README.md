# SARS-CoV-2 Nucleocapsid-Cytokine Docking Analyses

<h3 align="right">Tuple and MIT Lincoln Lab</h3>

Large scale, _in silico_ interaction analyses of SARS-CoV-2 nucleocapsid protein variants against human cytokines.

![](/img/Experiments.png)


## HADDOCK 2.4 Analyses

HADDOCK 2.4 was run on to dock the 1,088 combinations of 64 human cytokines × 17 N proteins. We refer to these combinations as "experiments".

Ambiguous Interaction Restraints (AIRs) were defined using a random selection of 20% of the surface residues on the input proteins. This was to reduce our input bias surrounding the docking site while reducing computation time.

HADDOCK generates 200 PDB complexes for each experiment in each of its three iterations:
1. Rigid body docking (it0)
2. Semi-flexible refinement (it1)
3. Solvent refinement in water (itw)

In the final water refinement step, the HADDOCK system will cluster the complexes and generate cluster-level metrics.

From these cluster-level metrics, we select the best cluster based on the lowest _van der Waals_ energy. Then, from this best cluster, we select the best (representative) PDB file as the one with the lowest _van der Waals_ energy.

### Results

- Experiment Results: [haddock/experiment_results.csv](haddock/experiment_results.csv)
- Best PDBs: [haddock/best_pdbs/](haddock/best_pdbs/)

### Resources

- Running HADDOCK 2.4 in an HPC environment: [haddock/README.md](haddock/README.md)
- HADDOCK 2.4 scoring function: https://www.bonvinlab.org/software/haddock2.4/scoring/
- HADDOCK 2.4 clustering logic: https://www.bonvinlab.org/software/haddock2.4/analysis/#cluster-based-analysis


## AlphaFold2 Multimer Analyses

### Results

- Experiment Results: [alphafold2_multimer/AF23_experiment_results.csv](alphafold2_multimer/AF23_experiment_results.csv)
- Best PDBs: [alphafold2_multimer/best_pdbs](alphafold2_multimer/best_pdbs)



## Data Explorer App

We have provided a basic data explorer that allows for the generation of figures and the viewing of the PDB complexes. This application is written in Streamlit. To run the application locally, run the following commands:

```sh
cd app/
streamlit run Home.py
```