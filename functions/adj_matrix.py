import numpy as np
import pandas as pd

def parse_edges(text):
    edges = []
    lines = text.strip().split(';')
    for line in lines:
        if '--' in line:
            parts = line.strip().split(' ')
            if len(parts) == 3 and '-->' in parts[2]:
                start_node = parts[0].strip('--')
                end_node = parts[2].strip('-->')
                weight = parts[1].strip()
                end_node = end_node.strip()
                edges.append((start_node, end_node, weight))
            else:
                print(f"Ошибка разбора строки: {line}")
    return edges

def create_adjacency_matrix(edges):
    vertices = sorted(set(sum([[edge[0], edge[1]] for edge in edges], [])))
    
    n = len(vertices)
    adj_matrix = pd.DataFrame(np.zeros((n, n)))
    
    index_map = {vertex: i for i, vertex in enumerate(vertices)}
    
    for start, end, weight in edges:
        i, j = index_map[start], index_map[end]
        try:
            adj_matrix.iloc[i, j] = float(weight)
        except:
            lambda_index = vertices[i] + vertices[j]
            adj_matrix.iloc[i, j] = str(weight+"_{" + f'{lambda_index}' + "}")  
    
    return adj_matrix, vertices
