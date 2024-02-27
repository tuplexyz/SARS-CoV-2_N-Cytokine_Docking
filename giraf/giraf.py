#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Graph-based Interface Residue Assessment Function (GIRAF)


Load INTERCAAT output file, parse the interactions.
Build a graph network from it!

Dependencies:
    pandas for INTERCAAT df parsing and creation
    networkx for graph networking
    matplotlib for plotting the figures from the manuscript

@author: Raf Jaimes, MIT Lincoln Lab
@date: 2023-09-07

"""
# %%
import os
import re

import pandas as pd

import networkx as nx

import matplotlib.pyplot as plt

# %% INTERCAAT File Loading

def parse_intercaat(filename, lut = None):
    """
    Args:
        filename (str): filename of the intercaat text file.
        lut (dataframe): lookup table with consensus sequence information

    Returns:
        interactions_df (pd.DataFrame): interactions dataframe

    """

    df = pd.read_fwf(filename, header=None)
    # the header is variable in length depending on the number of query residues
    # check column [0] for matching string.
    # after this row is all of the query and chain interactions
    idx = df[df[0] == 'Query Chain    |Interacting Chains|'].index[0]
    # the subset is everything after the header, only the interactions
    interactions = df[idx+1:]
    interactions.reset_index(inplace=True)
    
    # The first column now contains 8 columns. It is the most complicated
    # we need to split it up several ways to get all 8 cols out
    first_column = interactions[0].str.split('|', expand=True)
    split_0 = first_column[0].str.split(' ', expand=False)
    split_1 = first_column[1].str.split(' ', expand=False)
    
    # Now remove all the empty spaces
    split_0 = split_0.apply(lambda x: list(filter(None, x)))
    split_1 = split_1.apply(lambda x: list(filter(None, x)))
    
    # qc = query chain (typically, Chain A, e.g. nucleocapsid)
    # ic = interacting chain (typically, Chain B, C, etc. e.g. Cytokine)
    # now start to put everything together in a interactions_df
    interactions_df = pd.DataFrame(columns=['qc_aa', 'qc_res_num', 'qc_chain', 'qc_atomtype',
                                     'ic_aa', 'ic_res_num', 'ic_chain', 'ic_atomtype',
                                     'dist', 'atomclasses'])
    
    interactions_df[['qc_aa', 'qc_res_num', 'qc_chain', 'qc_atomtype']] = pd.DataFrame(data=split_0.tolist())
    interactions_df[['ic_aa', 'ic_res_num', 'ic_chain', 'ic_atomtype']] = pd.DataFrame(data=split_1.tolist())
             
    # dist is back in the 1 column of interactions
    interactions_df['dist'] = interactions[1]
    # atomclasses is back in the 3 column of interactions
    interactions_df['atomclasses'] = interactions[3]
    
    filebase = os.path.basename(filename)
    pattern = re.compile('^.*?(?=_)')
    n_protein = re.match(pattern,filebase).group(0)  
    
    p = 0
    interactions_df['qc_map_res_num'] = 0
    for p in range(0, len(interactions_df)):
        interactions_df['qc_map_res_num'].iloc[p] = lut['Consensus'].loc[lut[n_protein] == int(interactions_df['qc_res_num'].iloc[p])]
        p = p + 1
        
    interactions_df['qc_map_res_num'] = interactions_df['qc_map_res_num'].astype(str)
    
    return interactions_df

# %% Graph Network

def generate_graph(interactions_df, variables='just_aa', DIST_CUTOFF=3):     
    """
    Summary: Generate a graph object based on the residue interactions.
    
    Description: You should use a tool like INTERCAAT to find the residue
        interactions first. Then parse those outputs and compile them
        into a dataframe.
    
    Args:
        interactions_df (pd.DataFrame): interactions dataframe

    Returns:
        G (networkx.classes.graph.Graph): output network graph object

    """
    # New Graph
    G = nx.Graph()
    
    # You don't have to add Nodes explicitly, we can just create them
    # implicitly by adding Edges.        
        
    if variables=='all':
        # Uses all the interaction parameters, very busy graphs
        for p in range(0,len(interactions_df)):
            select = interactions_df.iloc[p]
        
            G.add_edges_from(
                [(select['qc_chain'] + select['qc_aa'] + select['qc_res_num'] + select['qc_atomtype'],
                  select['ic_chain'] + select['ic_aa'] + select['ic_res_num'] + select['ic_atomtype'],
                 {'weight' : interactions_df['dist']} )] )      
            
            p = p + 1
    
    elif variables=='no_atoms':
        # Makes the graphs simpler by removing the atom-level interactions
        # Maintains the AAs, residue numbering. Remove weight/distance.
        for p in range(0,len(interactions_df)):
            select = interactions_df.iloc[p]
        
            G.add_edges_from(
                [(select['qc_chain'] + ',' + select['qc_aa'] + select['qc_res_num'] ,
                  select['ic_chain'] + ',' + select['ic_aa'] + select['ic_res_num'] 
                  )] )  
            
            p = p + 1
            
    elif variables=='res_nums':
        # Makes the graphs simpler by removing the atom-level interactions
        # Maintains the AAs, residue numbering. Remove weight/distance.
        
        select = interactions_df[['qc_chain', 'ic_chain', 'qc_map_res_num', 'ic_res_num']].loc[interactions_df['dist'].astype(float) < DIST_CUTOFF]
        select.drop_duplicates(inplace=True)
        
        for p in range(0,len(select)):
            rowselect = select.iloc[p]
            qc_node = rowselect['qc_chain'] + ',' + rowselect['qc_map_res_num']
            ic_node = rowselect['ic_chain'] + ',' + rowselect['ic_res_num'] 
                
            G.add_nodes_from(
                [(qc_node, {'label' : qc_node}),
                  (ic_node, {'label' : ic_node})
                  ] )  
            
            G.add_edge(qc_node, ic_node)
            
            p = p + 1
               
    elif variables=='just_aa':
        # Simplest graphs. Removes distance parameter, residue#, and atoms.
        # Only retains the AA on Chain A (QC) and AA on Chain B (IC)
        just_aa_df = interactions_df[['qc_chain', 'qc_aa', 'ic_chain', 'ic_aa']]
        just_aa_df.drop_duplicates(inplace=True)
        for p in range(0,len(just_aa_df)):
            select = just_aa_df.iloc[p]         
                        
            G.add_edges_from(
                [(select['qc_chain'] + ',' + select['qc_aa'] ,
                  select['ic_chain'] + ',' + select['ic_aa'] )] )      
            
            p = p + 1       
            
        
    return G, interactions_df


# %%
def node_subst_cost(node1, node2):
    # check if the nodes are equal, if yes then apply no cost, else apply 3
    if node1['label'] == node2['label']:
        return 0
    return 1

# %% Exploration
from os import listdir

# LUT work
from preprocess_align import make_lut
 
lut = make_lut()

# Timeout set to 4 sec is approximately equivalent to 20 sec
# Runs much faster. You could try longer timeouts to see if GED minimizes further.
TIMEOUT=4
#TIMEOUT=20
VARIABLES='res_nums'

# %% Calculate all the GEDs for the AlphaFold2 INTERCAAT results
analysis_dir = 'CXCL12beta_analysis/AF2_INTERCAAT/'
file1 = 'SARS-CoV-2-WA1-N_CXCL12beta_relaxed_model_2_multimer_v3_pred_2.pdb_intercaat.txt'

df1 = parse_intercaat(analysis_dir + file1, lut)
graph1, idf = generate_graph(df1, variables=VARIABLES)


file_list = listdir(analysis_dir)

# num_ir is the number of interacting residues
af2_geds = pd.DataFrame(columns=['filename', 'ged','num_ir'])
for file2 in file_list:
    try:
        df2 = parse_intercaat(analysis_dir + file2, lut)
        graph2, idf = generate_graph(df2, variables=VARIABLES)
        print(file2)
        one_ged = nx.graph_edit_distance(graph1, graph2, timeout=TIMEOUT, node_subst_cost=node_subst_cost)
        
        # num_ir counting on the N protein
        A_chain=list()
        for key in graph2._node:
             if key.startswith("A"):
                 A_chain.append(key)                 
        num_ir = len(A_chain)
        
        af2_geds = pd.concat([af2_geds, pd.DataFrame(data=[[file2, one_ged,num_ir]], columns=['filename', 'ged', 'num_ir'])])
    except:
        print('error with ' + file2)
    finally:
        continue
    
af2_geds.reset_index(inplace=True)
af2_geds['n_protein'] = af2_geds['filename'].str.split('_', expand=True).iloc[:,0]
af2_geds.set_index('n_protein', inplace=True)
af2_geds.sort_values(by='n_protein', ascending=True, inplace=True)


# %% Calculate all the GEDs for the HADDOCK INTERCAAT results
analysis_dir = 'CXCL12beta_analysis/HADDOCK_INTERCAAT/'

# Best File = SARS-CoV-2-BA.1.1-N_CXCL11_model_4_multimer_v3_pred_4
#file1 = 'SARS-CoV-2-BA.1.1-N_CXCL11_relaxed_model_4_multimer_v3_pred_4.pdb_intercaat.txt'
#file1 = 'SARS-CoV-N_CXCL12beta_relaxed_model_1_multimer_v3_pred_1.pdb_intercaat.txt'

file1 = 'SARS-CoV-2-WA1-N__CXCL12beta_165w.pdb_intercaat.txt'


# original omicron
#file1 = 'SARS-CoV-2-B.1.1.529-N_CXCL12beta_relaxed_model_2_multimer_v3_pred_2.pdb_intercaat.txt'

df1 = parse_intercaat(analysis_dir + file1, lut)
graph1, idf = generate_graph(df1, variables=VARIABLES)


file_list = listdir(analysis_dir)

# num_ir is the number of interacting residues
haddock_geds = pd.DataFrame(columns=['filename', 'ged','num_ir'])
for file2 in file_list:
    try:
        df2 = parse_intercaat(analysis_dir + file2, lut)
        graph2, idf = generate_graph(df2, variables=VARIABLES)
        print(file2)
        one_ged = nx.graph_edit_distance(graph1, graph2, timeout=TIMEOUT, node_subst_cost=node_subst_cost)
        
        # num_ir counting on the N protein
        A_chain=list()
        for key in graph2._node:
             if key.startswith("A"):
                 A_chain.append(key)                 
        num_ir = len(A_chain)
        
        haddock_geds = pd.concat([haddock_geds, pd.DataFrame(data=[[file2, one_ged,num_ir]], columns=['filename', 'ged', 'num_ir'])])
    finally:
        continue
    
haddock_geds.reset_index(inplace=True)
haddock_geds['n_protein'] = haddock_geds['filename'].str.split('_', expand=True).iloc[:,0]
haddock_geds.set_index('n_protein', inplace=True)
haddock_geds.sort_values(by='n_protein', ascending=True, inplace=True)

# %% Comparing HADDOCK to AF2

analysis_dir = 'CXCL12beta_analysis/'
haddock_dir = 'HADDOCK_INTERCAAT/'
af2_dir = 'AF2_INTERCAAT/'

haddock_file_list = listdir(analysis_dir + haddock_dir)
af2_file_list = listdir(analysis_dir + af2_dir)
haddock_file_list.sort()
af2_file_list.sort()

# ged is the graph edit distance
# num_ir is the number of interacting residues
geds = pd.DataFrame(columns=['filename', 'ged','haddock_num_ir', 'af2_num_ir'])
af2_index = 0
for haddock_file in haddock_file_list:
    try:
        af2_df = parse_intercaat(analysis_dir + af2_dir + af2_file_list[af2_index], lut)  
        af2_graph, idf = generate_graph(af2_df, variables=VARIABLES)
        
        haddock_df = parse_intercaat(analysis_dir + haddock_dir + haddock_file, lut)
        haddock_graph, idf = generate_graph(haddock_df, variables=VARIABLES)
        print(af2_file_list[af2_index] + ' vs. ' + haddock_file)
        one_ged = nx.graph_edit_distance(af2_graph, haddock_graph, timeout=TIMEOUT, node_subst_cost=node_subst_cost)
              
        # num_ir counting on the N protein
        A_chain=list()
        for key in haddock_graph._node:
             if key.startswith("A"):
                 A_chain.append(key)                 
        haddock_num_ir = len(A_chain)       
        
        # num_ir counting on the N protein
        A_chain=list()
        for key in af2_graph._node:
             if key.startswith("A"):
                 A_chain.append(key)                 
        af2_num_ir = len(A_chain)   
        
        
        geds = pd.concat([geds, pd.DataFrame(data=[[haddock_file, one_ged,haddock_num_ir, af2_num_ir ]], columns=['filename', 'ged', 'haddock_num_ir', 'af2_num_ir'])])
    finally:
        af2_index += 1
        continue
    
geds.reset_index(inplace=True)
geds['n_protein'] = geds['filename'].str.split('_', expand=True).iloc[:,0]
geds.set_index('n_protein', inplace=True)
geds.sort_values(by='ged', ascending=True, inplace=True)


# %% Plotting Bars for GEDs

fig = plt.figure(figsize=(14,9))

def get_axis_limits(ax):
    return ax.get_xlim()[0]*-0.5, ax.get_ylim()[1]*1.1

af2_geds.sort_values(by='ged', inplace=True)
subax1 = plt.subplot(221)
subax1.barh(af2_geds.index, af2_geds.ged)
subax1.set_xlabel('AlphaFold2 - GED from SARS-CoV-2-WA1 N')
subax1.set_title('A', loc='left', fontsize=16, fontweight='bold')

#subax1.annotate('A', xy=get_axis_limits(subax1), fontsize=14)

#ax.set_xlim([100, 200])
#ax.set_title(r'Best N <> CXCL12$\beta$ Compared to' '\n' r'SARS-CoV-2-XBB-N <> CXCL12$\beta$')

# Plotting Bars for Number of Interacting Residues

subax2 = plt.subplot(222)
haddock_geds.sort_values(by='ged', inplace=True)
subax2.barh(haddock_geds.index, haddock_geds.ged)
subax2.set_xlabel('HADDOCK - GED from SARS-CoV-2-WA1 N')
#ax.set_xlim([100, 200])
subax2.set_title('B', loc='left', fontsize=16, fontweight='bold')

# Plotting Bars for GEDs

#fig = plt.figure(figsize=(14,9))


geds.sort_values(by='ged', inplace=True)
subax1 = plt.subplot(223)
subax1.barh(geds.index, geds.ged)
subax1.set_xlabel('GED Between AlphaFold2 and HADDOCK')
subax1.set_title('C', loc='left', fontsize=16, fontweight='bold')
#subax1.annotate('A', xy=get_axis_limits(subax1), fontsize=14)

#ax.set_xlim([100, 200])
#ax.set_title(r'Best N <> CXCL12$\beta$ Compared to' '\n' r'SARS-CoV-2-XBB-N <> CXCL12$\beta$')

# Plotting Bars for Number of Interacting Residues

geds.sort_values(by='haddock_num_ir', inplace=True)
subax2 = plt.subplot(224)
subax2.barh(geds.index, geds.haddock_num_ir, label='HADDOCK', alpha=0.7)
subax2.barh(geds.index, geds.af2_num_ir, label='AlphaFold2', alpha=0.7)
subax2.set_xlabel(r'# of Interface Residues under 3Å')
#ax.set_xlim([100, 200])
subax2.set_title('D', loc='left', fontsize=16, fontweight='bold')

plt.legend()
fig.tight_layout(h_pad=3)

fig.savefig('GED_4panel.pdf')


# %% Bipartite Example

analysis_dir = 'CXCL12beta_analysis/HADDOCK_INTERCAAT/'
file1 = 'SARS-CoV-2-WA1-N__CXCL12beta_165w.pdb_intercaat.txt'
file2 = 'SARS-CoV-2-XBB-N__CXCL12beta_4w.pdb_intercaat.txt'

df_example1 = parse_intercaat(analysis_dir + file1, lut)  
graph2, idf = generate_graph(df_example1, variables=VARIABLES)

df_example2 = parse_intercaat(analysis_dir + file2, lut)  
graph2, idf = generate_graph(df_example2, variables=VARIABLES)

A_chain=list()
for key in graph1._node:
     if key.startswith("A"):
         A_chain.append(key)
         
B_chain=list()
for key in graph1._node:
     if key.startswith("B"):
         B_chain.append(key)

options = {"edgecolors": "tab:gray", "node_size": 2400, "alpha": 0.8}

fig = plt.figure(figsize=(14,6))
subax1 = plt.subplot(121)
nx.draw(graph1, pos=nx.bipartite_layout(graph1, nodes=B_chain, align='horizontal'), with_labels=True, node_color="tab:blue", **options ) 
subax1.set_title(r'(A) SARS-CoV-2-WA1 N', fontsize=20)
subax1.text(x=-0.2, y=-1.4, s=r'(B) CXCL12$\beta$', fontsize=20)

A_chain=list()
for key in graph2._node:
     if key.startswith("A"):
         A_chain.append(key)
         
B_chain=list()
for key in graph2._node:
     if key.startswith("B"):
         B_chain.append(key)

subax2 = plt.subplot(122)
nx.draw(graph2, pos=nx.bipartite_layout(graph2, nodes=B_chain, align='horizontal'), with_labels=True, node_color="tab:red", **options ) 
subax2.set_title(r'(A) SARS-CoV-2-XBB N ', fontsize=20)
subax2.text(x=-0.2, y=-1.33, s=r'(B) CXCL12$\beta$', fontsize=20)

plt.tight_layout()
plt.savefig('graph_bipartite.pdf')
