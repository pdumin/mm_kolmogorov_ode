import pandas as pd
import re
from functools import reduce
from collections import OrderedDict


def generate_from_matrix(adj_matrix: pd.DataFrame) -> str:
    """Generate ODE representation with latex from adjancecy matrix

    Args:
        adj_matrix (pd.DataFrame): adjancecy matrix of n x n size,
        where n is number of states

    Returns:
        str: latex code of equation system
    """
    equations = []
    n = len(adj_matrix)
    states = list(adj_matrix.columns)

    for i in range(n):
        equation_terms = []
        for j in range(n):
            if adj_matrix.values[j][i] != 0:
                equation_terms.append(
                    f"{adj_matrix.values[j][i]}  p_{{{states[j]}}}(t)"
                )
        for j in range(n):
            if adj_matrix.values[i][j] != 0:
                equation_terms.append(
                    f"-{adj_matrix.values[i][j]} p_{{{states[i]}}}(t)"
                )

        equation = (
            f"\\dfrac{{dp_{states[i]}}}{{dt}} = " + " + ".join(equation_terms)
            if equation_terms
            else f"p_{{{states[i]}}} = 0"
        )

        equations.append(equation.replace("+ -", "- "))

    ltx_code = "\\\\[10pt]".join([f"{eq} " for eq in equations])
    ltx_code = "\\begin{cases}\n" + ltx_code + "\\end{cases}"
    ltx_code = ltx_code.replace("\\[10pt]", "\\[10pt]\n")
    ltx_code = ltx_code.replace("}}", "}}\n")
    ltx_code = ltx_code.replace("\\end", "\n\\end")
    return ltx_code

def generate_from_mermaid(mermaid_code: str) -> str:
    """Generate ODE latex representation directly from mermaid code

    Args:
        mermaid_code (str): mermaid code

    Returns:
        str: latex code of equation system
    """    
    lines = mermaid_code.split(';')[1:-1]
    verticies = set(reduce(lambda x, y: x+y, [(i.strip()[0]+i.strip()[-1]) for i in lines]))

    terms = {k : v for k, v in zip(verticies, ['']*len(verticies))}
    for i in lines:
        out_state, intensity, in_state = re.sub(r'-->|--', '', i).strip().split()
        if not terms.get(out_state):
            terms[out_state] = f'\\dfrac{{dp_{out_state}}}{{dt}} = -{intensity}p_{{{out_state}}}(t) '
        else:
            terms[out_state] += f'- {intensity}p_{{{out_state}}}(t)'
        # print(f'dp{out_state} = -{out_state}*p{out_state}')    

    # in_terms = []
    for i in lines:
        out_state, intensity, in_state = re.sub(r'-->|--', '', i).strip().split()
        if terms[in_state] == '':
            terms[in_state] += f'\\dfrac{{dp_{in_state}}}{{dt}} = {intensity}p_{{{out_state}}}(t) '
        else:
            terms[in_state] += f'+ {intensity}p_{{{out_state}}}(t) '
    ode = OrderedDict(sorted(terms.items()))
    ltx_code = ''
    
    for k, v in ode.items():
        ltx_code += f'\n{v} \\\\[10pt]'
    ltx_code = ltx_code.strip()
    ltx_code = "\\begin{cases}\n" + ltx_code + "\n\\end{cases}"
    return ltx_code