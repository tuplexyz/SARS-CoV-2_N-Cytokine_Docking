## Calculate prodigy values

import os
import pandas as pd

candidates = pd.read_excel("Docking_Results.xlsx")

for index, candidate in candidates.iterrows():
    candidate_id = candidate['Candidate']
    if candidate_id not in ['Sacituzumab', 'Sacituzumab (Sun)']:
        best_pdb = candidate['best_struct']
        best_pdb_path = f"./predicted_structures/{candidate_id}/haddock_results/{best_pdb}"
        # print(best_pdb_path)
        # os.system(f"prodigy {best_pdb_path}")
        print(f"prodigy {best_pdb_path} > ./prodigy_results/{candidate_id}_prodigy.txt")

# prodigy ./predicted_structures/SG-154.1A4/haddock_results/data_50.pdb > ./prodigy_results/SG-154.1A4_prodigy.txt
# prodigy ./predicted_structures/SG-154.1B3/haddock_results/data_47.pdb > ./prodigy_results/SG-154.1B3_prodigy.txt
# prodigy ./predicted_structures/SG-154.1B5/haddock_results/data_60.pdb > ./prodigy_results/SG-154.1B5_prodigy.txt
# prodigy ./predicted_structures/SG-154.1C5/haddock_results/data_125.pdb > ./prodigy_results/SG-154.1C5_prodigy.txt
# prodigy ./predicted_structures/SG-154.1D11/haddock_results/data_163.pdb > ./prodigy_results/SG-154.1D11_prodigy.txt
# prodigy ./predicted_structures/SG-154.1D3/haddock_results/data_132.pdb > ./prodigy_results/SG-154.1D3_prodigy.txt
# prodigy ./predicted_structures/SG-154.1D8/haddock_results/data_115.pdb > ./prodigy_results/SG-154.1D8_prodigy.txt
# prodigy ./predicted_structures/SG-154.1D9/haddock_results/data_40.pdb > ./prodigy_results/SG-154.1D9_prodigy.txt
# prodigy ./predicted_structures/SG-154.1E5/haddock_results/data_45.pdb > ./prodigy_results/SG-154.1E5_prodigy.txt
# prodigy ./predicted_structures/SG-154.1F11/haddock_results/data_41.pdb > ./prodigy_results/SG-154.1F11_prodigy.txt
# prodigy ./predicted_structures/SG-154.1G11/haddock_results/data_122.pdb > ./prodigy_results/SG-154.1G11_prodigy.txt
# prodigy ./predicted_structures/SG-154.1G5/haddock_results/data_77.pdb > ./prodigy_results/SG-154.1G5_prodigy.txt
# prodigy ./predicted_structures/SG-154.1G8/haddock_results/data_135.pdb > ./prodigy_results/SG-154.1G8_prodigy.txt
# prodigy ./predicted_structures/SG-154.1H10/haddock_results/data_166.pdb > ./prodigy_results/SG-154.1H10_prodigy.txt
# prodigy ./predicted_structures/SG-154.2A1/haddock_results/data_181.pdb > ./prodigy_results/SG-154.2A1_prodigy.txt
# prodigy ./predicted_structures/SG-154.2A4/haddock_results/data_126.pdb > ./prodigy_results/SG-154.2A4_prodigy.txt
# prodigy ./predicted_structures/SG-154.2A6/haddock_results/data_103.pdb > ./prodigy_results/SG-154.2A6_prodigy.txt
# prodigy ./predicted_structures/SG-154.2A9/haddock_results/data_66.pdb > ./prodigy_results/SG-154.2A9_prodigy.txt
# prodigy ./predicted_structures/SG-154.2B11/haddock_results/data_79.pdb > ./prodigy_results/SG-154.2B11_prodigy.txt
# prodigy ./predicted_structures/SG-154.2B3/haddock_results/data_162.pdb > ./prodigy_results/SG-154.2B3_prodigy.txt
# prodigy ./predicted_structures/SG-154.2C1/haddock_results/data_164.pdb > ./prodigy_results/SG-154.2C1_prodigy.txt
# prodigy ./predicted_structures/SG-154.2C2/haddock_results/data_58.pdb > ./prodigy_results/SG-154.2C2_prodigy.txt
# prodigy ./predicted_structures/SG-154.2C3/haddock_results/data_12.pdb > ./prodigy_results/SG-154.2C3_prodigy.txt
# prodigy ./predicted_structures/SG-154.2C4/haddock_results/data_168.pdb > ./prodigy_results/SG-154.2C4_prodigy.txt
# prodigy ./predicted_structures/SG-154.2C5/haddock_results/data_121.pdb > ./prodigy_results/SG-154.2C5_prodigy.txt
# prodigy ./predicted_structures/SG-154.2E7/haddock_results/data_56.pdb > ./prodigy_results/SG-154.2E7_prodigy.txt
# prodigy ./predicted_structures/SG-154.2F2/haddock_results/data_49.pdb > ./prodigy_results/SG-154.2F2_prodigy.txt
# prodigy ./predicted_structures/SG-154.2F6/haddock_results/data_76.pdb > ./prodigy_results/SG-154.2F6_prodigy.txt
# prodigy ./predicted_structures/SG-154.2F8/haddock_results/data_155.pdb > ./prodigy_results/SG-154.2F8_prodigy.txt
# prodigy ./predicted_structures/SG-154.2G7/haddock_results/data_180.pdb > ./prodigy_results/SG-154.2G7_prodigy.txt
# prodigy ./predicted_structures/SG-154.2G9/haddock_results/data_147.pdb > ./prodigy_results/SG-154.2G9_prodigy.txt
# prodigy ./predicted_structures/SG-154.2H1/haddock_results/data_117.pdb > ./prodigy_results/SG-154.2H1_prodigy.txt
# prodigy ./predicted_structures/SG-154.2H11/haddock_results/data_62.pdb > ./prodigy_results/SG-154.2H11_prodigy.txt
# prodigy ./predicted_structures/SG-154.2H3/haddock_results/data_76.pdb > ./prodigy_results/SG-154.2H3_prodigy.txt
# prodigy ./predicted_structures/SG-154.2H8/haddock_results/data_61.pdb > ./prodigy_results/SG-154.2H8_prodigy.txt
# prodigy ./predicted_structures/SG-155.1B11/haddock_results/data_83.pdb > ./prodigy_results/SG-155.1B11_prodigy.txt
# prodigy ./predicted_structures/SG-155.1D4/haddock_results/data_117.pdb > ./prodigy_results/SG-155.1D4_prodigy.txt
# prodigy ./predicted_structures/SG-155.1D8/haddock_results/data_195.pdb > ./prodigy_results/SG-155.1D8_prodigy.txt
# prodigy ./predicted_structures/SG-155.1F8/haddock_results/data_64.pdb > ./prodigy_results/SG-155.1F8_prodigy.txt
# prodigy ./predicted_structures/SG-155.1H5/haddock_results/data_194.pdb > ./prodigy_results/SG-155.1H5_prodigy.txt
# prodigy ./predicted_structures/SG-155.1H7/haddock_results/data_119.pdb > ./prodigy_results/SG-155.1H7_prodigy.txt
# prodigy ./predicted_structures/SG-155.2A6/haddock_results/data_117.pdb > ./prodigy_results/SG-155.2A6_prodigy.txt
# prodigy ./predicted_structures/SG-155.2A9/haddock_results/data_36.pdb > ./prodigy_results/SG-155.2A9_prodigy.txt
# prodigy ./predicted_structures/SG-155.2B10/haddock_results/data_143.pdb > ./prodigy_results/SG-155.2B10_prodigy.txt
# prodigy ./predicted_structures/SG-155.2E1/haddock_results/data_47.pdb > ./prodigy_results/SG-155.2E1_prodigy.txt
# prodigy ./predicted_structures/SG-155.2E4/haddock_results/data_109.pdb > ./prodigy_results/SG-155.2E4_prodigy.txt
# prodigy ./predicted_structures/SG-155.2F4/haddock_results/data_6.pdb > ./prodigy_results/SG-155.2F4_prodigy.txt
# prodigy ./predicted_structures/SG-155.2F6/haddock_results/data_84.pdb > ./prodigy_results/SG-155.2F6_prodigy.txt
# prodigy ./predicted_structures/SG-155.2F9/haddock_results/data_156.pdb > ./prodigy_results/SG-155.2F9_prodigy.txt
# prodigy ./predicted_structures/SG-155.2H1/haddock_results/data_166.pdb > ./prodigy_results/SG-155.2H1_prodigy.txt

## Read each Prodigy output and get binding affinity and dissociation constant.
affinity_output = {}
for file in os.listdir("./prodigy_results"):
    if file.endswith("_prodigy.txt"):
        # print(file)
        candidate_id = file.replace("_prodigy.txt", "")
        results = pd.read_table(f"./prodigy_results/{file}", sep="~", names = ["item"])
        for index, result in results.iterrows():
            if result["item"].startswith("[++] Predicted binding affinity (kcal.mol-1):"):
                ba = float(result["item"].replace("[++] Predicted binding affinity (kcal.mol-1):", "").replace(" ", ""))
                # print(ba)
            if result["item"].startswith("[++] Predicted dissociation constant (M) at 25.0˚C:"):
                dc = float(result["item"].replace("[++] Predicted dissociation constant (M) at 25.0˚C:", "").replace(" ", ""))
                # print(dc)
    output_iter = {"binding_affinity": ba, "dissociation_constant": dc }
    # print(output_iter)
    affinity_output[candidate_id] = output_iter

affinity_df = pd.DataFrame.from_dict(affinity_output, orient='index')
affinity_df['candidate'] = affinity_df.index


affinity_df.to_csv("./prodigy_results/prodigy_scores.csv")