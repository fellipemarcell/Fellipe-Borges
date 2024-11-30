import numpy as np

def calculate_exact_solution (nodes):
    """
    Função para calcular a solução exata do problema.

    Parâmetros
    ----------
        nodes : ndarray
            Coordenadas dos nós da malha.

    Retorna
    -------
        u_exact : ndarray
            Solução exata nos nós da malha.
    """
    
    if nodes is None:
        raise ValueError("Nós da malha não podem ser vazios")
    
    # if not isinstance(nodes, np.ndarray):
    #     raise TypeError("Nós da malha devem ser um array numpy")
    
    # if nodes.ndim != 2:
    #     raise ValueError("Nós da malha devem ser um array numpy de duas dimensões")
    
    u_exact = np.empty(len(nodes))
    for i, node in enumerate(nodes):
        if node is None:
            raise ValueError("Nós da malha não podem ser vazios")
        
        if not isinstance(node, np.ndarray):
            raise TypeError("Nós da malha devem ser um array numpy")
        
        if node.ndim != 1:
            raise ValueError("Nós da malha devem ser um array numpy de uma dimensão")
        
        if node.shape[0] != 2:
            raise ValueError("Nós da malha devem ter dimensão igual a 2")
        
        u_exact[i] = np.sin(np.pi * node[0]) * np.sin(np.pi * node[1])

    return u_exact