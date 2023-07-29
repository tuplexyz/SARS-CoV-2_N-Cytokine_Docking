import streamlit as st
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
def load_haddock_data():
    data = pd.read_csv("../postprocessing/experiment_results.csv")
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
st.subheader('HADDOCK Protein Docking Viewer')

stcol1, stcol2= st.columns(2)

## Create a text element message
data_load_state = st.sidebar.text('Loading HADDOCK results...')

## Load HADDOCK Data
haddock_data = load_haddock_data()

## Get list of N proteins
n_proteins = haddock_data.n_protein.sort_values().unique().tolist()
## Get list of Cytokine proteins
cytokine_proteins = haddock_data.cytokine_protein.sort_values().unique().tolist()

## List HADDOCK metrics of interest
haddock_metrics = [
    "Evdw+0.1Eelec",
    # "Evdw+0.1Eelec_sd",
    "Evdw",
    # "Evdw_sd",
    "Eelec",
    # "Eelec_sd",
    "Eair",
    # "Eair_sd",
    "Edesolv",
    # "Edesolv_sd",
    "AIRviol",
    # "AIRviol_sd",
    # "dihedviol",
    # "dihedviol_sd",
    "BSA",
    # "BSA_sd",
    "haddock-score",
    # "haddock-score_sd",
    "prodigy_deltaG_kcalpermol",
    "prodigy_dissociation_constant_M"
]

## Get Best PDBs list
best_pdbs = os.listdir("../postprocessing/best_pdbs")

## Update text element message
data_load_state.text('✔ HADDOCK results loaded.')


metrics_selection = st.sidebar.multiselect(
    'Select HADDOCK Metrics',
    haddock_metrics
)

haddock_selected_columns = [
    "n_protein",
    "cytokine_protein"
] + metrics_selection

with stcol1:
    # st.dataframe(haddock_data[haddock_selected_columns].sort_values(metrics_selection, ascending=True))
    haddock_df_selection = aggrid_interactive_table(df = haddock_data[haddock_selected_columns].sort_values(metrics_selection, ascending=True))
    if len(haddock_df_selection["selected_rows"]) > 0:
        n_protein_selection = haddock_df_selection["selected_rows"][0]["n_protein"]
        cytokine_protein_selection = haddock_df_selection["selected_rows"][0]["cytokine_protein"]

with stcol2:
    if len(haddock_df_selection["selected_rows"]) > 0:
        st.write(f"{n_protein_selection} (in orange) docked with {cytokine_protein_selection} (in cyan):")
        best_pdb_file = list(filter(lambda x: x.startswith(f'{n_protein_selection}__{cytokine_protein_selection}'), best_pdbs))[0]

        with open(f"../postprocessing/best_pdbs/{best_pdb_file}") as pdb_file:
            pdb_data = "".join([x for x in pdb_file])

        pdbview = py3Dmol.view(width=800, height=800) 
        pdbview.addModelsAsFrames(pdb_data)
        pdbview.setBackgroundColor("#0E1117")
        pdbview.setStyle( {'chain':'A'}, { 'cartoon': {'color': '#FFA500' }})
        pdbview.setStyle( {'chain':'B'}, { 'cartoon': {'color': '#00FFFF'}})
        pdbview.zoomTo()
        showmol(pdbview, width = 800, height = 800)