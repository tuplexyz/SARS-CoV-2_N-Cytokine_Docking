#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 13 13:02:54 2023

@author: raflocal
"""
# %%
import numpy as np
import pandas as pd


msa = pd.read_fwf('BetaCoV-N-MSA.txt', header=None)
names = msa[0].unique()

msa2 = pd.DataFrame(index=names, columns=['sequence'])
for name in names:
    extract = msa[2].loc[msa[0] == name]
    msa2['sequence'].loc[msa2.index == name] = extract.str.cat(sep='')
