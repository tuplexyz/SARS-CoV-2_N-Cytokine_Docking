import streamlit as st
from streamlit_js_eval import streamlit_js_eval
import plotly.express as px
import py3Dmol
from stmol import *
from st_aggrid import AgGrid, GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode
import sys
import pandas as pd

st.set_page_config(
    layout="wide",
    page_title="1. Protein Viewer",
    page_icon="🔍",
)

@st.cache_data
def load_experiment_data():
    data = pd.read_csv("../full_experiment_results.csv")
    return data

def aggrid_interactive_table(df: pd.DataFrame):
    """Creates an st-aggrid interactive table based on a dataframe.
    SOURCE: https://github.com/streamlit/example-app-interactive-table/blob/main/streamlit_app.py
    Args:
        df (pd.DataFrame]): Source dataframe

    Returns:
        dict: The selected row
    """
    options = GridOptionsBuilder.from_dataframe(
        df, enableRowGroup=True, enableValue=True, enablePivot=True
    )

    options.configure_side_bar()

    options.configure_selection("single")
    selection = AgGrid(
        df,
        width='100%',
        height=800, 
        enable_enterprise_modules=False,
        gridOptions=options.build(),
        # theme="light",
        update_mode=GridUpdateMode.MODEL_CHANGED,
        # allow_unsafe_jscode=True,
    )
    return selection

st.title('SARS-CoV-2 Nucleocapsid-Cytokine Docking Analyses')
st.subheader('Protein Docking Viewer')

## Set number of columns
stcol1, stcol2, stcol3 = st.columns(3, gap="small")

## Get screen height and width
screen_width = int(streamlit_js_eval(js_expressions='screen.width'))
view_width = 0.25 * screen_width
# screen_height = int(streamlit_js_eval(js_expressions='screen.height'))

## Create a text element message
data_load_state = st.sidebar.text('Loading results...')

## Load Experiment Data
experiment_data = load_experiment_data()

## Get list of N proteins
n_proteins = experiment_data.n_protein.sort_values().unique().tolist()
## Get list of Cytokine proteins
cytokine_proteins = experiment_data.cytokine_protein.sort_values().unique().tolist()

## List HADDOCK metrics of interest
experiment_metrics = [
    "haddock_Evdw+0.1Eelec",
    "haddock_Evdw",
    "haddock_Eelec",
    "haddock_Eair",
    "haddock_Edesolv",
    "haddock_AIRviol",
    "haddock_dihedviol",
    "haddock_BSA",
    "haddock-score",
    "haddock_prodigy_deltaG_kcalpermol",
    "haddock_prodigy_dissociation_constant_M",
    "haddock_foldx_intraclashes_group1",
    "haddock_foldx_intraclashes_group2",
    "haddock_foldx_deltaG_kcalpermol",
    "haddock_foldx_stability_group1",
    "haddock_foldx_stability_group2",
    "dist_from_SARS-CoV-2-WA1-N_A",
    "af2_iptm+ptm",
    "af2_gdock",
    "af2_total_score",
    "af2_IntraclashesGroup1",
    "af2_IntraclashesGroup2",
    "af2_foldx_dG",
    "af2_Backbone Hbond",
    "af2_Sidechain Hbond",
    "af2_Van der Waals",
    "af2_Electrostatics",
    "af2_Solvation Polar",
    "af2_Solvation Hydrophobic",
    "af2_Van der Waals clashes",
    "af2_entropy sidechain",
    "af2_entropy mainchain",
    "af2_sloop_entropy",
    "af2_mloop_entropy",
    "af2_cis_bond",
    "af2_torsional clash",
    "af2_backbone clash",
    "af2_helix dipole",
    "af2_water bridge",
    "af2_disulfide",
    "af2_electrostatic kon",
    "af2_partial covalent bonds",
    "af2_energy Ionisation",
    "af2_Entropy Complex",
    "af2_Number of Residues",
    "af2_Interface Residues",
    "af2_Interface Residues Clashing",
    "af2_Interface Residues VdW Clashing",
    "af2_Interface Residues BB Clashing",
    "af2_prodigy_deltaG_kcalpermol",
    "af2_prodigy_dissociation_constant_M"
]

## Get Best PDBs lists
haddock_best_pdbs = os.listdir("../haddock/postprocessing/best_pdbs")
af2_best_pdbs = os.listdir("../alphafold2_multimer/best_AF2_and_GDock")

## Update text element message
data_load_state.text('✔ Experiment results loaded.')


metrics_selection = st.sidebar.multiselect(
    'Select Experiment Metrics',
    experiment_metrics
)
prefix_note = st.sidebar.caption('Note: The `haddock` prefix denotes a score from the HADDOCK experiments and the `af2` prefix denotes a score from the AlphaFold2-Multimer experiments.')

experiment_selected_columns = [
    "n_protein",
    "cytokine_protein"
] + metrics_selection

## Data Panel
with stcol1:
    experiment_df_selection = aggrid_interactive_table(df = experiment_data[experiment_selected_columns].sort_values(metrics_selection, ascending=True))
    if len(experiment_df_selection["selected_rows"]) > 0:
        n_protein_selection = experiment_df_selection["selected_rows"][0]["n_protein"]
        cytokine_protein_selection = experiment_df_selection["selected_rows"][0]["cytokine_protein"]



## HADDOCK Panel
with stcol2:
    if len(experiment_df_selection["selected_rows"]) > 0:
        st.markdown(f"#### HADDOCK Prediction:")
        haddock_best_pdb_file = list(filter(lambda x: x.startswith(f'{n_protein_selection}__{cytokine_protein_selection}'), haddock_best_pdbs))[0]

        with open(f"../haddock/postprocessing/best_pdbs/{haddock_best_pdb_file}") as pdb_file:
            haddock_pdb_data = "".join([x for x in pdb_file])

        haddock_pdbview = py3Dmol.view(width = view_width, height = 600) 
        haddock_pdbview.addModelsAsFrames(haddock_pdb_data)
        haddock_pdbview.setBackgroundColor("#0E1117")
        haddock_pdbview.setStyle( {'chain':'A'}, { 'cartoon': {'color': '#FFBE45' }})
        haddock_pdbview.setStyle( {'chain':'B'}, { 'cartoon': {'color': '#60B5FF'}})
        haddock_pdbview.zoomTo()
        showmol(haddock_pdbview, width = view_width, height = 600)

        st.markdown(f'### :orange[{n_protein_selection}] & :blue[{cytokine_protein_selection}]')
        st.write(f"{n_protein_selection} (in orange) docked with {cytokine_protein_selection} (in cyan).")

## AlphaFold2 Panel
with stcol3:
    if len(experiment_df_selection["selected_rows"]) > 0:
        st.markdown(f"#### AlphaFold2-Multimer Prediction:")
        af2_best_pdb_file = list(filter(lambda x: x.startswith(f'{n_protein_selection}_{cytokine_protein_selection}'), af2_best_pdbs))[0]

        with open(f"../alphafold2_multimer/best_AF2_and_GDock/{af2_best_pdb_file}") as pdb_file:
            af2_pdb_data = "".join([x for x in pdb_file])

        af2_pdbview = py3Dmol.view(width = view_width, height = 599) 
        af2_pdbview.addModelsAsFrames(af2_pdb_data)
        af2_pdbview.setBackgroundColor("#0E1117")
        af2_pdbview.setStyle( {'chain':'A'}, { 'cartoon': {'color': '#FFBE45' }})
        af2_pdbview.setStyle( {'chain':'B'}, { 'cartoon': {'color': '#60B5FF'}})
        af2_pdbview.zoomTo()
        showmol(af2_pdbview, width = view_width, height = 600)