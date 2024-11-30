import gmsh
import numpy as np
import matplotlib.pyplot as plt

def generate_mesh(size, refinement_level, element_type, order):
    """
    Gera uma malha quadrangular regular de n lados e ordenada de Lagrange.

    Args:
    - size (float): Tamanho do lado do domínio quadrado.
    - refinement_level (int): Nível de refinamento.
    - element_type (str): Tipo de elemento ('tri' ou 'quad').
    - order (int): Ordem do polinômio de Lagrange.

    Returns:
    - nodes (ndarray): Array de vértices da malha.
    - elements (ndarray): Array de elementos da malha.
    """
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

        if not gmsh.isInitialized():
            gmsh.initialize()

        # Criar um quadrado para a malha
        if not gmsh.model.add("Mesh"):
            raise ValueError("Erro ao adicionar o modelo 'Mesh'")

        lc = size / (refinement_level ** 2)

        # Definir os pontos do quadrado
        try:
            p1 = gmsh.model.geo.addPoint(0, 0, 0, lc)
            p2 = gmsh.model.geo.addPoint(size, 0, 0, lc)
            p3 = gmsh.model.geo.addPoint(size, size, 0, lc)
            p4 = gmsh.model.geo.addPoint(0, size, 0, lc)
        except Exception as e:
            raise ValueError(f"Erro ao adicionar os pontos do quadrado: {e}") from e

        # Criar as linhas do quadrado
        try:
            l1 = gmsh.model.geo.addLine(p1, p2)
            l2 = gmsh.model.geo.addLine(p2, p3)
            l3 = gmsh.model.geo.addLine(p3, p4)
            l4 = gmsh.model.geo.addLine(p4, p1)
        except Exception as e:
            raise ValueError(f"Erro ao adicionar as linhas do quadrado: {e}") from e

        # Criar o loop da superfície
        try:
            loop = gmsh.model.geo.addCurveLoop([l1, l2, l3, l4])
            surface = gmsh.model.geo.addPlaneSurface([loop])
        except Exception as e:
            raise ValueError(f"Erro ao adicionar o loop da superfície: {e}") from e

        # Sincronizar a geometria
        if not gmsh.model.geo.synchronize():
            raise ValueError("Erro ao sincronizar a geometria")

        # Definir a ordem do polinômio de Lagrange
        if not gmsh.option.setNumber("Mesh.ElementOrder", order):
            raise ValueError("Erro ao definir a ordem do polinômio de Lagrange")

        # Definir opções de recomposição se necessário
        if element_type == "quad":
            if not gmsh.option.setNumber("Mesh.RecombineAll", 1):
                raise ValueError("Erro ao definir a opção de recomposição")
            if not gmsh.model.mesh.setRecombine(2, surface):
                raise ValueError("Erro ao definir a opção de recomposição para a superfície")

        # Gerar a malha
        if not gmsh.model.mesh.generate(2):
            raise ValueError("Erro ao gerar a malha")

        # Obter nós e elementos da malha
        try:
            node_tags, node_coords, _ = gmsh.model.mesh.getNodes()
            element_types, element_tags, element_node_tags = gmsh.model.mesh.getElements(2)
        except Exception as e:
            raise ValueError(f"Erro ao obter os nós e elementos da malha: {e}") from e

        nodes = np.array(node_coords).reshape((-1, 3))[:, :2]

        # Verificar o tipo de elementos e ajustá-los corretamente
        if element_type == "tri":
            for i, elem_type in enumerate(element_types):
                if elem_type == 2:  # 2 é o código para elementos triangulares
                    try:
                        elements = np.array(element_node_tags[i]).reshape((-1, 3))
                    except Exception as e:
                        raise ValueError(f"Erro ao obter os elementos triangulares: {e}") from e
                    break
        elif element_type == "quad":
            for i, elem_type in enumerate(element_types):
                if elem_type == 3:  # 3 é o código para elementos quadrangulares
                    try:
                        elements = np.array(element_node_tags[i]).reshape((-1, 4))
                    except Exception as e:
                        raise ValueError(f"Erro ao obter os elementos quadrangulares: {e}") from e
                    break
    
    except Exception as e:
        raise ValueError(f"Erro ao gerar a malha: {e}") from e

    finally:
        if gmsh.isInitialized():
            gmsh.finalize()

    # Retornar os nós e elementos da malha                
    return nodes, elements

# Exemplo 1: Geração de uma malha com os parâmetros a seguir
size = 1.0  # tamanho do quadrado
refinement_level = 3  # nível de refinamento
element_type = "tri"  # tipo de elemento (tri ou quad)
order = 2  # ordem do polinômio de Lagrange

# Gerar a malha
nodes, elements = generate_mesh(size, refinement_level, element_type, order)

# Imprimir os nós e elementos da malha
print("Nós da malha:")
print(nodes)
print("\nElementos da malha:")
print(elements)

# Plotar a malha (opcional)
import matplotlib.pyplot as plt
plt.figure(figsize=(8, 8))
plt.scatter(nodes[:, 0], nodes[:, 1], s=10)
for element in elements:
    plt.plot(nodes[element, 0], nodes[element, 1], 'b-')
plt.axis('equal')
plt.show()