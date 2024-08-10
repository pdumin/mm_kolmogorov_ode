import pyperclip
import streamlit as st
from streamlit_mermaid import st_mermaid
from streamlit_monaco import st_monaco

from functions.adj_matrix import create_adjacency_matrix, parse_edges
from functions.eq_generation import generate_from_matrix, generate_from_mermaid

if not 'user_code' in st.session_state.keys():
    st.session_state['user_code'] = None

if not 'adj_matrix' in st.session_state.keys():
    st.session_state['adj_matrix'] = None

st.set_page_config(
    layout="wide",
    page_icon="⚙️"
)

st.title("Mermaid construction")

def draw(inp_code):
    st_mermaid(inp_code, height="250px", width="400px")

def latex_copy(inp_code):
    pyperclip.copy(inp_code)
    st.toast('Latex code was succsessfully copied to clipboard!')

col1, col2 = st.columns([.4, .6])

with col1:
    mermaid_code = """graph LR;
    a-- 0.5 -->b;
    a-- 0.5 -->c;
    b-- 0.5 -->d;
    b-- 0.5 -->e;
    c-- 0.5 -->e;
    c-- 0.5 -->d;
    d-- 0.5 -->f;
    d-- 0.5 -->g;
    e-- 0.5 -->g;
    e-- 0.5 -->f;
    """
    user_code = st_monaco(value=mermaid_code, height="300px", language="markdown")
    st.session_state['user_code'] = user_code
    

with col2:
    draw(user_code)

source = st.radio('Source', ['Mermaid code', 'Adjancecy matrix'])
gen_matrix_btn = st.button('Generate matrix')



lcol, rcol = st.columns(2)


if gen_matrix_btn:
    if source == 'Mermaid code':
        result = generate_from_mermaid(user_code)
        lcol.code(result)
        rcol.latex(result)
    if source == 'Adjancecy matrix':
        edges = parse_edges(user_code)
        frame, verticies = create_adjacency_matrix(edges)
        frame.columns = verticies
        frame.index = verticies
        ltx_code = generate_from_matrix(adj_matrix=frame)
        json_tab, matrix_tab, latex_tab = lcol.tabs(['JSON', 'Matrix', 'LaTeX'])
        with latex_tab:
            st.code(ltx_code)
            st.button('Copy to clipboard', on_click=latex_copy, args=(ltx_code, ))
        with json_tab:
            st.session_state['adj_matrix'] = frame.values
            st.json(edges, expanded=False)
        with matrix_tab: 
            st.table(frame)
        rcol.latex(ltx_code)