import gmsh
import numpy as np
import matplotlib.pyplot as plt

def generate_mesh2(size, refinement_level, element_type, order):
    gmsh.initialize()
    model = gmsh.model
    mesh = model.mesh

    # Criar um quadrado para a malha
    p1 = model.geo.add_point(0, 0, 0, size)
    p2 = model.geo.add_point(size, 0, 0, size)
    p3 = model.geo.add_point(size, size, 0, size)
    p4 = model.geo.add_point(0, size, 0, size)

    l1 = model.geo.add_line(p1, p2)
    l2 = model.geo.add_line(p2, p3)
    l3 = model.geo.add_line(p3, p4)
    l4 = model.geo.add_line(p4, p1)

    loop = model.geo.add_curve_loop([l1, l2, l3, l4])
    surface = model.geo.add_plane_surface([loop])

    # Sincronizar a geometria
    model.geo.synchronize()

    # Definir a ordem do polinômio de Lagrange
    mesh.set_order(order)

    # Gerar a malha
    mesh.generate(2)

    # Obter nós e elementos da malha
    node_tags, node_coords, _ = mesh.get_nodes()
    element_types, element_tags, element_node_tags = mesh.get_elements(2)

    # Converter os elementos para um formato mais fácil de usar
    elements = np.array(element_node_tags)
    elements = elements.reshape((-1, 4))

    # Retornar os nós e elementos da malha
    return node_coords, elements

# Exemplo de uso
size = 1.0
refinement_level = 1
element_type = "quad"
order = 2

node_coords, elements = generate_mesh2(size, refinement_level, element_type, order)

# Imprimir os nós e elementos da malha
print("Nós da malha:")
print(node_coords)
print("\nElementos da malha:")
print(elements)

# Plotar a malha (opcional)
plt.figure(figsize=(8, 8))
plt.scatter(node_coords[::3], node_coords[1::3], s=10)
for element in elements:
    x = [node_coords[element[i]-1] for i in range(4)]
    y = [node_coords[element[i]-1+1] for i in range(4)]
    plt.plot(x, y, 'b-')
plt.axis('equal')
plt.show()

gmsh.finalize()