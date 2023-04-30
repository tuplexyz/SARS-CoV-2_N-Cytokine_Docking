from pymol import cmd
from random import sample
from helper_scripts.find_random_surface_residues import find_random_surface_residues
from helper_scripts.make_air_file import write_air_file


## Wu1-CXCL12beta Example
N_file = 'C:\\Users\\Colby\\Documents\\GitHub\\SARS-CoV-2_N-Cytokine_Docking\\manual_tests\\Wu-1_CXCL12beta_inDocker\\SARS-CoV-2_N_Wu1.pdb'
cytokine_file = 'C:\\Users\\Colby\\Documents\\GitHub\\SARS-CoV-2_N-Cytokine_Docking\\manual_tests\\Wu-1_CXCL12beta_inDocker\\CXCL12beta.pdb'

N_residues = find_random_surface_residues(file = N_file, percentage = 0.25)
'''
N_residues = [1, 9, 19, 20, 23, 24, 25, 26, 30, 33, 37, 38, 39, 44, 58, 67, 69, 70, 75, 98, 99, 
103, 125, 129, 131, 132, 135, 136, 140, 141, 143, 144, 146, 151, 155, 163, 164, 167, 
168, 178, 189, 190, 198, 199, 202, 204, 205, 209, 211, 217, 219, 224, 226, 230, 234, 
236, 237, 239, 240, 242, 244, 252, 253, 254, 255, 260, 265, 267, 275, 276, 278, 282, 
298, 299, 314, 318, 320, 324, 327, 328, 334, 343, 346, 347, 349, 351, 354, 357, 360, 
362, 364, 376, 379, 381, 382, 384, 391, 413, 416, 417]
'''

cytokine_residues = find_random_surface_residues(file = cytokine_file, percentage = 0.25)
'''
cytokine_residues = [1, 3, 11, 12, 20, 34, 35, 47, 49, 50, 53, 55, 61, 63, 64, 65, 67]
'''

write_air_file(active1 = N_residues,
               passive1 = [],
               active2 = cytokine_residues,
               passive2 = [],
               segid1='A', segid2='B',
               output_file = "C:\\Users\\Colby\\Documents\\GitHub\\SARS-CoV-2_N-Cytokine_Docking\\manual_tests\\Wu-1_CXCL12beta_inDocker\\air.tbl")