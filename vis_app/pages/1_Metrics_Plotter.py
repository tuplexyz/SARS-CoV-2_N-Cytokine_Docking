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
    page_title="2. Metrics Plotter",
    page_icon="📊",
)

@st.cache_data
def load_haddock_data():
    data = pd.read_csv("../full_experiment_results.csv")
    return data

st.title('SARS-CoV-2 Nucleocapsid-Cytokine Docking Analyses')
st.subheader('HADDOCK Metrics Plotter')

## Create a text element message
data_load_state = st.sidebar.text('Loading HADDOCK results...')

## Load HADDOCK Data
haddock_data = load_haddock_data()
n_proteins = haddock_data.n_protein.sort_values().unique().tolist()
cytokine_proteins = haddock_data.cytokine_protein.sort_values().unique().tolist()
haddock_metrics = [
    "haddock_Evdw+0.1Eelec",
    "haddock_Evdw",
    "haddock_Eelec",
    "haddock_Eair",
    "haddock_Edesolv",
    "haddock_AIRviol",
    "haddock_BSA",
    "haddock-score",
    "haddock_prodigy_deltaG_kcalpermol",
    "haddock_prodigy_dissociation_constant_M"
]
# best_pdbs = os.listdir("../haddock/postprocessing/best_pdbs")

## Update text element message
data_load_state.text('✔ HADDOCK results loaded.')

slice_by_selection = st.sidebar.selectbox(
    'Slice By...',
    ('N Proteins', 'Cytokines')
)

if slice_by_selection == 'N Proteins':
    # n_selection = st.sidebar.selectbox(
    #     'N Protein',
    #     n_proteins
    # )
    category_selection = "n_protein"
    color_by_selection = "cytokine_protein"
    
elif slice_by_selection == 'Cytokines':
    # cytokine_selection = st.sidebar.selectbox(
    #     'Cytokine Protein',
    #     cytokine_proteins
    # )
    category_selection = "cytokine_protein"
    color_by_selection = "n_protein"

metric_selection = st.sidebar.selectbox(
    'Select HADDOCK Metric',
    haddock_metrics
)

plot_selection = st.sidebar.multiselect(
    'Select Plot Type(s)',
    ('Table', 'Boxplot', '3D Scatter')
)

if "Table" in plot_selection:
    st.dataframe(haddock_data)


if "Boxplot" in plot_selection:
    ## Make Boxpot
    plt_haddock_boxplot = px.box(
        haddock_data,
        # orientation = 'h',
        x = category_selection,
        y = metric_selection,
        # color = color_by_selection#,
        color = category_selection,
        points = "all",
        title = f"Boxplot: {metric_selection} by {slice_by_selection}"
    ).update_xaxes(categoryorder = "median ascending")

    plt_haddock_boxplot.update_layout(showlegend=False,
                                      height=800)

    st.plotly_chart(plt_haddock_boxplot,
                    height=800,
                    use_container_width=True)

if "3D Scatter" in plot_selection:

    plt_haddock_3d_scatter = px.scatter_3d(
        haddock_data,
        x = 'n_protein',
        y = 'cytokine_protein',
        z = metric_selection,
        color = metric_selection,
        # symbol = category_selection,
        title = f"3D Scatterplot: {metric_selection}"
    )
    plt_haddock_3d_scatter.update_layout(showlegend=False,
                                         height=1000)

    st.plotly_chart(plt_haddock_3d_scatter,
                    height=1000,
                    use_container_width=True)
