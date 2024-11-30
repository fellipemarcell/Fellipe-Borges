import numpy as np

def apply_dirichlet(K, F, vertices):
    """
    Aplica as condições de contorno de Dirichlet em uma matriz rigidez (K) e um vetor força (F), 
    considerando que as condições de contorno são impostas na borda do domínio delimitado 
    pelos vértices dados em 'vertices'.
    
    Parameters:
    K (numpy array): Matriz de rigidez do sistema.
    F (numpy array): Vetor de força do sistema.
    vertices (list of tuples): Lista de vértices do domínio, onde cada vértice é uma tupla (x, y) 
        com as coordenadas do vértice.
    
    Returns:
    K (numpy array): Matriz de rigidez do sistema com as condições de contorno de Dirichlet 
        aplicadas.
    F (numpy array): Vetor de força do sistema com as condições de contorno de Dirichlet 
        aplicadas.
    """
    # Verifica se as entradas são vazias
    if K is None or F is None or vertices is None:
        raise ValueError("Matriz K, vetor F, ou vértices não podem ser vazios")

    # # Verifica se as entradas são matrizes e vetores numpy
    # if not isinstance(K, np.ndarray) or not isinstance(F, np.ndarray):
    #     raise TypeError("Matriz K e vetor F devem ser matrizes e vetores numpy")

    # Verifica se as entradas possuem as dimensões corretas
    if K.ndim != 2 or F.ndim != 1:
        raise ValueError("Matriz K e vetor F devem ter dimensões 2 e 1, respectivamente")

    # Verifica se as entradas possuem as mesmas dimensões
    if K.shape[0] != K.shape[1] or K.shape[0] != F.shape[0]:
        raise ValueError("Matriz K e vetor F devem ter as mesmas dimensões")

    # Aplica as condições de contorno de Dirichlet    
    boundary_nodes = [i for i, (x, y) in enumerate(vertices) if x in [0, 1] or y in [0, 1]]

    for node in boundary_nodes:
        if node < 0 or node >= len(F):
            raise IndexError("Índice de nó fora do intervalo")
        K[node, :] = 0
        K[:, node] = 0
        K[node, node] = 1
        F[node] = 0

    return K, F    