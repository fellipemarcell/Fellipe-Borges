from matplotlib import pyplot as plt

def plot_mesh(nodes, elements, display):
    """
    Plota a malha de elementos finitos.
    
    Args:
    - nodes (ndarray): Array de vértices da malha.
    - elements (ndarray): Array de elementos da malha.
    - display (str): Opção de exibição:
        - "no": Não plota a malha.
        - "mesh": Plota apenas a malha.
        - "nodes": Plota a malha e os nós.
        - "val": Plota a malha e numera os nós.
    """
    
    if nodes is None or elements is None:
        raise ValueError("Nodes and elements cannot be None")

    if display not in ["no", "mesh", "nodes", "val"]:
        raise ValueError("Invalid display option")

    plt.figure(figsize=(8, 8))

    # Plotar os elementos ligando os vértices por linhas
    for elem in elements:
        if elem is None:
            raise ValueError("Elements cannot be None")
        elem_vertices = nodes[elem - 1, :]  # Ajustar índice para zero-based
        for i in range(len(elem)):
            x = [elem_vertices[i, 0], elem_vertices[(i + 1) % len(elem), 0]]
            y = [elem_vertices[i, 1], elem_vertices[(i + 1) % len(elem), 1]]
            plt.plot(x, y, 'k-', linewidth=0.7)  # 'k-' para linhas pretas
    
    if display == "no":
        quit()
    if display == "mesh":
        pass 
    elif display == "nodes":
        # Plotar os nós
        plt.scatter(nodes[:, 0], nodes[:, 1], c='red', s=10, label='Nós')
    elif display == 'val':
        # Numerando os nós
        for i, (x, y) in enumerate(nodes):
            plt.text(x, y, f'{i+1}', fontsize=8, ha='right', va='top')
    
    plt.gca().set_aspect('equal', adjustable='box')
    plt.title('Malha de Elementos Finitos')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.show()