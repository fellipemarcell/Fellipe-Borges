
def num_nodes_element(type_element, order):
    """
    Calcula o número total de nós no elemento.

    Args:
    - type_element (str): Tipo de elemento: triangular ou quadrilátero ('tri' ou 'quad').
    - order (int): Ordem do polinômio de Lagrange.

    Returns:
    - nodes_element (int): Número de nós no elemento.
    """
    # Verifica se o tipo de elemento é válido
    if type_element not in ["tri", "quad"]:
        raise ValueError("Type element must be 'tri' or 'quad'.")
    
    # Verifica se a ordem do polinômio é inteiro e maior que zero
    if order < 1:
        raise ValueError("Order must be a positive integer.")
    
    # Calcula o número de nós no interior e nas arestas do elemento
    if type_element == "tri":
        num_sides = 3
    elif type_element == "quad":
        num_sides = 4
    
    # Calcula o número de nós no interior e nas arestas do elemento
    num_edge_nodes = order - 1  # Nós adicionais por aresta
    nodes_element = (num_sides * (num_edge_nodes + 1)) + (order - 1) * (order - 2) // 2  # Total de nós (vértices + nós interiores)
    
    return nodes_element

# # Exemplo:
# type_element = "tri"
# order = 3
# nodes_element = num_nodes_element(type_element, order)
# print(nodes_element) 

# # Saída: 12