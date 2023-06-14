import pandas as pd
import glob, os

directory_prefix = 'run1/structures/it1/water/'

## Get best cluster based on lowest van der Waals energy
vdw_clusters = pd.read_csv(f'{directory_prefix}cluster_ener.txt', delimiter=r"\s+").sort_values(by=['Evdw'], ascending = True)
best_cluster = vdw_clusters.iat[0, 0]

## Get best PDB file from best cluster
cluster_pdbs = pd.read_csv(f'{directory_prefix}{best_cluster}_ener', delimiter=r"\s+").sort_values(by=['Evdw'], ascending = True)
best_pdb = cluster_pdbs.iat[0, 0]

## Make list of files to keep
all_cluster_files = glob.glob(f'{directory_prefix}cluster_*')
all_clusters_files = glob.glob(f'{directory_prefix}clusters*')
best_cluster_files = glob.glob(f'{directory_prefix}{best_cluster}_*')

files_to_keep = [
    'clusters.stat',
    best_pdb
] + all_cluster_files + all_clusters_files + best_cluster_files

files_to_keep_w_dir = [directory_prefix + f for f in files_to_keep]

## Clean up unwanted files
for root, dirs, files in os.walk('run1'):
    for file in files:
        file_path = os.path.join(root, file)
        if file_path in files_to_keep:
            print(f'+ Keeping: {file_path}')
        else:
            print(f'- Removing: {file_path}')
            os.remove(file_path)

## Clean up empty folders
for folder, _, _ in list(os.walk('run1'))[::-1]:
    if len(os.listdir(folder)) == 0:
        print(f'- Removing Folder: {folder}')
        os.rmdir(folder)