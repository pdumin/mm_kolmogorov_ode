import pandas as pd

def generate_markov_equations(adj_matrix: pd.DataFrame) -> str:
    """Generate ODE representation with latex 

    Args:
        adj_matrix (pd.DataFrame): adjancecy matrix of n x n size,
        where n is number of states

    Returns:
        str: latex code for body of equation system
    """    
    equations = []
    n = len(adj_matrix)
    states = list(adj_matrix.columns)
    
    for i in range(n):
        equation_terms = []
        
        # Положительные слагаемые (переходы в текущее состояние)
        for j in range(n):
            if adj_matrix.values[j][i] != 0:
                equation_terms.append(f"{adj_matrix.values[j][i]}  p_{{{states[j]}}}(t)")
        
        # Отрицательные слагаемые (переходы из текущего состояния)
        for j in range(n):
            if adj_matrix.values[i][j] != 0:
                equation_terms.append(f"-{adj_matrix.values[i][j]} p_{{{states[i]}}}(t)")
        
        equation = f"\dfrac{{dp_{states[i]}}}{{dt}} = " + " + ".join(equation_terms) if equation_terms else f"p_{{{states[i]}}} = 0"

        equations.append(equation.replace('+ -', '- '))

    ltx_code = "\\\\[10pt]".join([f"{eq} " for eq in equations])
    ltx_code = "\\begin{cases}\n" + ltx_code + "\end{cases}"
    ltx_code = ltx_code.replace('\\[10pt]', '\\[10pt]\n')
    ltx_code = ltx_code.replace('}}', '}}\n')
    ltx_code = ltx_code.replace('\end', '\n\\end')
    
    return ltx_code