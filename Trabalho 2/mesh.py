import gmsh
import numpy as np
import matplotlib.pyplot as plt

def generate_mesh(size, refinement_level, element_type, order):
    """
    Gera a malha usando Gmsh com os parâmetros fornecidos.

    Args:
    - size (float): Tamanho do domínio quadrado.
    - refinement_level (int): Nível de refinamento da malha.
    - element_type (str): Tipo de elementos para gerar ('tri' para triangular, 'quad' para quadrilátero).
    - order (int): Ordem do polinômio de Lagrange.

    Returns:
    - nodes (ndarray): Vetor de vértices da malha.
    - elements (ndarray): Vetor de elementos da malha.
    """
    # Verificar os parâmetros
    try:
        # Verificar se o tamanho do lado do quadrado é maior que zero
        if size <= 0:
            raise ValueError("Erro: O tamanho do lado do quadrado deve ser maior que zero")

        # Verificar se o nível de refinamento é maior que zero
        if refinement_level <= 0:
            raise ValueError("Erro: O nível de refinamento deve ser maior que zero")

        # Verificar se o tipo de elemento é válido
        if element_type not in ["tri", "quad"]:
            raise ValueError("Erro: O tipo de elemento deve ser 'tri' ou 'quad'")

        # Verificar se a ordem do polinômio de Lagrange é maior que zero
        if order <= 0:
            raise ValueError("Erro: A ordem do polinômio de Lagrange deve ser maior que zero")
    except:
        pass

    # Inicializar o Gmsh
    try:
        gmsh.initialize()
    except Exception as e:
        raise ValueError(f"Erro ao inicializar o Gmsh: {e}") from e

    # Criar um domínio para a malha
    try:
        gmsh.model.add("Mesh")
    except Exception as e:
        raise ValueError(f"Erro ao criar o domínio para a malha: {e}") from e

    # Definir o tamanho do domínio
    try:
        lc = size / (refinement_level ** 2)
    except Exception as e:
        raise ValueError(f"Erro ao calcular o tamanho da malha: {e}") from e

    # Definir os pontos do domínio
    try:            
        p1 = gmsh.model.geo.addPoint(0, 0, 0, lc)
        p2 = gmsh.model.geo.addPoint(size, 0, 0, lc)
        p3 = gmsh.model.geo.addPoint(size, size, 0, lc)
        p4 = gmsh.model.geo.addPoint(0, size, 0, lc)
    except Exception as e:
        raise ValueError(f"Erro ao adicionar os pontos do domínio: {e}") from e

    # Criar as linhas do domínio
    try:
        l1 = gmsh.model.geo.addLine(p1, p2)
        l2 = gmsh.model.geo.addLine(p2, p3)
        l3 = gmsh.model.geo.addLine(p3, p4)
        l4 = gmsh.model.geo.addLine(p4, p1)
    except Exception as e:
        raise ValueError(f"Erro ao criar as linhas do domínio: {e}") from e

    # Criar o loop da superfície
    try:
        loop = gmsh.model.geo.addCurveLoop([l1, l2, l3, l4])
        surface = gmsh.model.geo.addPlaneSurface([loop])
    except Exception as e:
        raise ValueError(f"Erro ao criar o loop da superfície: {e}") from e

    # Sincronizar a geometria
    try:
        gmsh.model.geo.synchronize()
    except Exception as e:
        raise ValueError(f"Erro ao sincronizar a geometria: {e}") from e

    # Definir a ordem do polinômio de Lagrange
    try:
        gmsh.option.setNumber("Mesh.ElementOrder", order)
    except Exception as e:
        raise ValueError(f"Erro ao definir a ordem do polinômio de Lagrange: {e}") from e

    # Definir opções de recomposição se necessário
    if element_type == "quad":
        try:
            gmsh.option.setNumber("Mesh.RecombineAll", 1)
            gmsh.model.mesh.setRecombine(2, surface)
        except Exception as e:
            raise ValueError(f"Erro ao definir as opções de recomposição: {e}") from e

    # Gerar a malha
    try:
        gmsh.model.mesh.generate(2)
    except Exception as e:
        raise ValueError(f"Erro ao gerar a malha: {e}") from e

    # Obter nós e elementos da malha
    try:
        node_tags, node_coords, _ = gmsh.model.mesh.getNodes()
        element_types, element_tags, element_node_tags = gmsh.model.mesh.getElements(2)
    except Exception as e:
        raise ValueError(f"Erro ao obter serviços da malha: {e}") from e

    # Converter os resultados para numpy arrays
    try:
        nodes = np.array(node_coords).reshape((-1, 3))[:, :2]
    except Exception as e:
        raise ValueError(f"Erro ao converter os resultados para numpy arrays: {e}") from e

    # Verificar o tipo de elementos e ajustá-los corretamente
    try:    
        if element_type == "tri":
            elements = []
            for i, elem_type in enumerate(element_types):
                if elem_type == 2:  # 2 é o código para elementos triangulares
                    elements = np.array(element_node_tags[i]).reshape((-1, 3))
                    break
        else:    
            elements = []        
            for i, elem_type in enumerate(element_types):    
                if elem_type == 3:  # 3 é o código para elementos quadriláteros 
                    elements = np.array(element_node_tags[i]).reshape((-1, 4))
                    break
    except Exception as e:
        raise ValueError(f"Erro ao verificar o tipo de elementos e ajustá-los corretamente: {e}") from e

    # Finalizar o Gmsh
    try:
        gmsh.finalize()
    except Exception as e:
        raise ValueError(f"Erro ao finalizar o Gmsh: {e}") from e

    return nodes, elements

def plot_mesh(nodes, elements, display):
    """
    Plota a malha de elementos finitos.
    
    Args:
    - nodes (ndarray): Vetor de vértices da malha.
    - elements (ndarray): Vetor de elementos da malha.
    - display (str): Opção de exibição:
        - "no": Não plota a malha.
        - "mesh": Plota apenas a malha.
        - "nodes": Plota a malha e os nós.
        - "val": Plota a malha e numera os nós.
    """
    # Criar uma figura
    try:
        plt.figure(figsize=(8, 8))
    except Exception as e:
        raise ValueError(f"Erro ao criar a figura: {e}") from e

    # Plotar os elementos ligando os vértices por linhas
    try:
        for elem in elements:
            elem_vertices = nodes[elem - 1, :]  # Ajustar índice para zero-based
            for i in range(len(elem)):
                x = [elem_vertices[i, 0], elem_vertices[(i + 1) % len(elem), 0]]
                y = [elem_vertices[i, 1], elem_vertices[(i + 1) % len(elem), 1]]
                plt.plot(x, y, 'k-', linewidth=0.7)  # 'k-' para linhas pretas
    except Exception as e:
        raise ValueError(f"Erro ao plotar os elementos: {e}") from e
   
    # Plotar a malha
    try:
        if display == 'no':
            quit()
        if display == 'mesh':
            pass 
        elif display == 'nodes':
            # Plotar os nós
            plt.scatter(nodes[:, 0], nodes[:, 1], c='red', s=10, label='Nós')
        elif display == 'val':
            # Numerando os nós
            for i, (x, y) in enumerate(nodes):
                plt.text(x, y, f'{i+1}', fontsize=8, ha='right', va='top')
    except Exception as e:
        raise ValueError(f"Erro ao plotar a malha: {e}") from e
    
    # Configurar o gráfico
    try:
        plt.gca().set_aspect('equal', adjustable='box')
        plt.title('Malha de Elementos Finitos')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.show()
    except Exception as e:
        raise ValueError(f"Erro ao configurar o gráfico: {e}") from e

# # Parâmetros de exemplo
# size = 1.0  # Tamanho do domínio quadrado
# refinement_level = 2  # Nível de refinamento da malha
# element_type = 'quad' # Escolha do tipo de elemento: "triangle" para triangular ou "quad" para quadrilátero
# order = 1  # Ordem do polinômio de interpolação de Lagrange

# # Gerar a malha usando Gmsh
# nodes, elements = generate_mesh(size, refinement_level, element_type, order)

# # Exibir os nós e elementos gerados
# display = 'mesh' # Exibir malha ("mesh"), malha e nós ("nodes") ou malha e numeração dos nós ("val")
# print("Nós da malha:")
# print(nodes)
# print("Elementos da malha:")
# print(elements)

# # Plotar a malha
# plot_mesh(nodes, elements, display)