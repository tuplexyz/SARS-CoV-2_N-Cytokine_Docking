# GIRAF: Graph-based Interface Residue Assessment Function  
This algorithm constructs bipartite graph networks that capture the interfacing residues between two chains in a protein complex.  
GIRAF was designed and works out of the box for INTERCAAT outputs, but could be adapted to other methods.  

Once the graphs are created, you can calculate the graph edit distance (GED) between any pair of graphs to quantify the similarity of the binding interactions.  

## Getting started  
Mamba was used to create a virtual env:  

```
mamba env create -n giraf  
mamba activate giraf  
mamba install networkx pandas matplotlib
```  

The following versions of packages were used:  
 *Python 3.11
 *NetworkX 3.1
 *Pandas 2.0.3
 *Matplotlib 3.7.1  

By default, the script will perform the analysis and display the figures shown in the manuscript.  

## LEGAL  
This material is based upon work supported by the Department of the Air Force under Air Force Contract No. FA8702-15-D-0001. Any opinions, findings, conclusions or recommendations expressed in this material are those of the author(s) and do not necessarily reflect the views of the Department of the Air Force.

© 2023 Massachusetts Institute of Technology.

The software/firmware is provided to you on an As-Is basis

Delivered to the U.S. Government with Unlimited Rights, as defined in DFARS Part 252.227-7013 or 7014 (Feb 2014). Notwithstanding any copyright notice, U.S. Government rights in this work are defined by DFARS 252.227-7013 or DFARS 252.227-7014 as detailed above. Use of this work other than as specifically authorized by the U.S. Government may violate any copyrights that exist in this work.
