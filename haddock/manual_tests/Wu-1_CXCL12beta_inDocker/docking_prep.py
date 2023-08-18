from pymol import cmd
from random import sample
from helper_scripts.find_random_surface_residues import find_random_surface_residues
from helper_scripts.make_air_file import write_air_file
from helper_scripts.make_run_params import write_run_params

## Wu1-CXCL12beta Example
N_file = 'C:\\Users\\Colby\\Documents\\GitHub\\SARS-CoV-2_N-Cytokine_Docking\\manual_tests\\Wu-1_CXCL12beta_inDocker\\SARS-CoV-2_N_Wu1.pdb'
cytokine_file = 'C:\\Users\\Colby\\Documents\\GitHub\\SARS-CoV-2_N-Cytokine_Docking\\manual_tests\\Wu-1_CXCL12beta_inDocker\\CXCL12beta.pdb'

N_residues = find_random_surface_residues(file = N_file, percentage = 0.5)
'''
N_residues = [1, 9, 19, 20, 23, 24, 25, 26, 30, 33, 37, 38, 39, 44, 58, 67, 69, 70, 75, 98, 99, 
103, 125, 129, 131, 132, 135, 136, 140, 141, 143, 144, 146, 151, 155, 163, 164, 167, 
168, 178, 189, 190, 198, 199, 202, 204, 205, 209, 211, 217, 219, 224, 226, 230, 234, 
236, 237, 239, 240, 242, 244, 252, 253, 254, 255, 260, 265, 267, 275, 276, 278, 282, 
298, 299, 314, 318, 320, 324, 327, 328, 334, 343, 346, 347, 349, 351, 354, 357, 360, 
362, 364, 376, 379, 381, 382, 384, 391, 413, 416, 417]
'''

cytokine_residues = find_random_surface_residues(file = cytokine_file, percentage = 1.0)
'''
cytokine_residues = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 
                    14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 
                    25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 
                    36, 37, 39, 41, 42, 43, 44, 45, 46, 47, 48, 
                    49, 50, 52, 53, 54, 55, 56, 57, 59, 60, 61, 
                    62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72]
'''

## Write our AIR file
write_air_file(active1 = N_residues,
               passive1 = [],
               active2 = cytokine_residues,
               passive2 = [],
               segid1='A', segid2='B',
               output_file = "C:\\Users\\Colby\\Documents\\GitHub\\SARS-CoV-2_N-Cytokine_Docking\\manual_tests\\Wu-1_CXCL12beta_inDocker\\air.tbl")


## Make run.param file
write_run_params(ambig_tbl = "./air.tbl",
                 haddock_dir = "/root/haddock/haddock2.4-2021-01/",
                 n_comp = 2,
                 pdb_file_1 = "./SARS-CoV-2_N_Wu1.pdb",
                 pdb_file_2 = "./CXCL12beta.pdb",
                 project_dir = "./",
                 prot_segid_1 = "A",
                 prot_segid_2 = "B",
                 run_number = 1,
                 output_file = "run.param")