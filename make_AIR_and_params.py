import shutil, os
from subprocess import Popen, PIPE
import pandas as pd
from helper_scripts.make_air_file import write_air_file
from helper_scripts.make_run_params import write_run_params

candidates = pd.read_excel("Docking_Results.xlsx")
# candidates = pd.read_excel("Docking_Results.xlsx").head(1)

## Write AIR file for each candidate using active and passive residues
for index, candidate in candidates.iterrows():
    candidate_id = candidate['Candidate']
    target_id = candidate['Target']
    active1 = candidate['Fab Active Residues'].split(',')
    passive1 = []
    active2 = candidate['Target Active Residues'].split(',')
    passive2 = []
    candidate_path = f"./predicted_structures/{candidate_id}/"
    air_file_name = f"{candidate_id}-{target_id}_air.tbl"
    write_air_file(active1, passive1, active2, passive2, segid1='A', segid2='B', output_file = f"{candidate_path}{air_file_name}")


## Write run.param file for each candidate
for index, candidate in candidates.iterrows():
    candidate_id = candidate['Candidate']
    target_id = candidate['Target']
    candidate_path = f"./predicted_structures/{candidate_id}/"
    air_file_name = f"{candidate_id}-{target_id}_air.tbl"
    write_run_params(ambig_tbl = air_file_name,
                     haddock_dir = "/root/haddock/haddock2.4-2021-01/",
                     n_comp = 2,
                     pdb_file_1 = f"./{candidate_id}_combined.pdb",
                     pdb_file_2 = "./7e5n_chainA.pdb",
                     project_dir = "./",
                     prot_segid_1 = "A",
                     prot_segid_2 = "B",
                     run_number = 1,
                     output_file = f"{candidate_path}run.param")


## Copy HADDOCK Scripts and Target PDB to each candidate directory
for index, candidate in candidates.iterrows():
    candidate_id = candidate['Candidate']
    candidate_path = f"./predicted_structures/{candidate_id}/"
    shutil.copyfile("./haddock_resources/run-docking.csh", f"{candidate_path}run-docking.csh")
    shutil.copytree("./haddock_resources/ana_scripts", f"{candidate_path}ana_scripts", dirs_exist_ok=True)
    shutil.copyfile("./7e5n_chainA.pdb", f"{candidate_path}7e5n_chainA.pdb")


## Create Docker Containers
# for index, candidate in candidates.iterrows():
for index, candidate in candidates.iloc[0:10, ].iterrows():
# for index, candidate in candidates.iloc[10:20, ].iterrows():
# for index, candidate in candidates.iloc[20:30, ].iterrows():
# for index, candidate in candidates.iloc[30:40, ].iterrows():
# for index, candidate in candidates.iloc[40:50, ].iterrows():
    candidate_id = candidate['Candidate']
    run_path = f"{os.getcwd()}\predicted_structures\{candidate_id}"
    os.system(f"docker run -v {run_path}:/data --name haddock2_4_{candidate_id} -d haddock2_4")

##  Execute HADDOCK Runs
# candidate_id = 'SG-154.1F11'
# for index, candidate in candidates.iterrows():
for index, candidate in candidates.iloc[0:10, ].iterrows():
# for index, candidate in candidates.iloc[10:20, ].iterrows():
# for index, candidate in candidates.iloc[20:30, ].iterrows():
# for index, candidate in candidates.iloc[30:40, ].iterrows():
# for index, candidate in candidates.iloc[40:50, ].iterrows():
    candidate_id = candidate['Candidate']
    # os.system(f'docker exec -it haddock2_4_{candidate_id} /data/run-docking.csh')
    # Popen(['docker', 'exec', '-it', f'haddock2_4_{candidate_id}', '/data/run-docking.csh'], stdout=PIPE, stderr=PIPE)

# docker exec -it haddock2_4_SG-154.1A4 /bin/tcsh
# docker exec -it haddock2_4_SG-154.1A4 /data/run-docking.csh


## Create Docker Containers and Execute HADDOCK Runs
# for index, candidate in candidates.iloc[0:10, ].iterrows():
# for index, candidate in candidates.iloc[10:20, ].iterrows():
# for index, candidate in candidates.iloc[20:30, ].iterrows():
# for index, candidate in candidates.iloc[30:40, ].iterrows():
# for index, candidate in candidates.iloc[40:50, ].iterrows():
for index, candidate in candidates.iterrows():
    candidate_id = candidate['Candidate']
    run_path = f"{os.getcwd()}\predicted_structures\{candidate_id}"
    os.system(f"docker run -v {run_path}:/data --name haddock2_4_{candidate_id} -d haddock2_4")
    os.system(f'docker exec -it haddock2_4_{candidate_id} /data/run-docking.csh')

