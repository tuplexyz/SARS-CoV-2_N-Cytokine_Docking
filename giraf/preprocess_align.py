#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# %%
import numpy as np
import pandas as pd

pd.options.mode.chained_assignment = None 


def make_lut(filename='BetaCoV-N-MSA.txt'):
    """
    Preprocessing step. Takes an MSA file from Geneious in and remaps it 
    into a clean look-up table (lut) which can be exported as a CSV.
    
    The CSV can later be used in the main GIRAF routine to map INTERCAAT 
    files against the Consensus sequence.

    @author: raflocal
    @date: 2023-10-13
    """

    # %% MSA File Loading
    
    pre_msa = pd.read_fwf(filename, header=None)
    names = pre_msa[0].unique()
    
    msa = pd.DataFrame(index=names, columns=['sequence'])
    for name in names:
        extract = pre_msa[2].loc[pre_msa[0] == name]
        msa['sequence'].loc[msa.index == name] = extract.str.cat(sep='')
    
    msa['n_protein'] = [np.nan, 'OC43-N', 'BANAL-20-52-N', 'MERS-CoV-N', 
                        'RaTG13-N', 'SARS-CoV-2-B.1.1.7-N', 'SARS-CoV-2-B.1.1-N', 
                        'SARS-CoV-2-B.1.351-N', 'SARS-CoV-2-B.1.617.2-DeltaA-N',
                        'SARS-CoV-2-P.1-N', 'SARS-CoV-2-BA.1.1-N',
                        'SARS-CoV-2-BA.2-N', 'SARS-CoV-2-BA.4-N',
                        'SARS-CoV-2-BQ.1-N', 'SARS-CoV-2-XBB-N',
                        'SARS-CoV-2-B.1.1.529-N','SARS-CoV-2-WA1-N', 'SARS-CoV-N']            
    
    # %%    
    consensus_order = pd.Series(range(0,len(msa['sequence'].iloc[0])))    
    
    # Lookup Table (lut) for mapping consensus residue # to variant residue #
    # Columns:
        # Consensus - consensus residue number
        # 'variant name' - the variant residue number, named for the n_protein
    
    # Note that p starts at 1 here.
    # The consensus sequence MUST be in row 0.
    p = 1;
    lut = pd.DataFrame(data=consensus_order, columns=['Consensus'])
    while p <= len(msa)-1:
    #while p <= 2:
        variant = msa['n_protein'].iloc[p]
        lut[variant] = np.nan
        print('Making LUT for ' + msa['n_protein'].iloc[p])
        count = 0;
        for m in range(0,len(msa['sequence'].iloc[p])):
            
            # Check if there is a point mutation
            if msa['sequence'].iloc[p][m].isalpha():
                lut[variant].iloc[m] = count
                count = count + 1;
            
            # check if it's same as consensus
            elif msa['sequence'].iloc[p][m] in '.' :
               lut[variant].iloc[m] = count
               count = count + 1;
                
            # check if there's a deletion        
            elif msa['sequence'].iloc[p][m] in '-' :
                continue                
            
        p = p +1
        
    # add 1 to every value so that the residue # starts at 1    
    lut += 1      
    return lut
    
    
