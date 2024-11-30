import numpy as np
from numpy.polynomial.legendre import leggauss

def gauss_points1(num_nodes_element, num_sides):
    """
    Calcula os pontos de Gauss e os pesos a partir do número total de nós do elemento e da ordem especificadas.
    
    Args:
    - num_nodes_element (int): O número de pontos do elemento.
    - num_sides (int): O número de lados do polígono regular.
    
    Returns:
    - gauss_points (list of tuples): Lista de tuplas contendo os pontos de Gauss (xi, yi) e os pesos correspondentes.
    """
    points, weights = leggauss(num_nodes_element)  # Obtém os pontos e pesos de Gauss-Legendre para a ordem especificada
    gauss_points = []  # Inicializa a lista de pontos de Gauss

    angles = np.linspace(0, 2 * np.pi, num_sides, endpoint=False)  # Calcula os ângulos dos vértices do polígono regular
    vertices = [(np.cos(angle), np.sin(angle)) for angle in angles]  # Calcula as coordenadas dos vértices do polígono

    for i in range(num_sides):
        v0 = np.array(vertices[i])  # Obtém o vértice atual
        v1 = np.array(vertices[(i + 1) % num_sides])  # Obtém o próximo vértice, considerando o polígono circular
        for p, w in zip(points, weights):
            xi = (1 - p) / 2  # Mapeia os pontos de Gauss de [-1, 1] para [0, 1]
            x = v0 + xi * (v1 - v0)  # Calcula a posição do ponto de Gauss ao longo da aresta do polígono
            gauss_points.append((x[0], x[1], w / num_sides))  # Adiciona o ponto de Gauss e o peso à lista

    for i in range(num_sides):
        v0 = np.array(vertices[i])  # Obtém o vértice atual
        v1 = np.array(vertices[(i + 1) % num_sides])  # Obtém o próximo vértice
        v2 = np.array([0, 0])  # Considera o centro do polígono como vértice adicional
        for pi, wi in zip(points, weights):
            for pj, wj in zip(points, weights):
                x = v0 * (1 - pi - pj) + v1 * pi + v2 * pj  # Calcula a posição do ponto de Gauss dentro do triângulo
                weight = wi * wj / (2 * num_sides)  # Calcula o peso ajustado para o triângulo
                gauss_points.append((x[0], x[1], weight))  # Adiciona o ponto de Gauss e o peso à lista
    
    return gauss_points  # Retorna a lista de pontos de Gauss e pesos

# # Exemplo de uso:
# num_nodes_element = 3
# num_sides = 4
# gauss_points_list = gauss_points1(num_nodes_element, num_sides)
# for point in gauss_points_list:
#     print(point)

import matplotlib.pyplot as plt

num_nodes_element = 5
num_sides = 6
gauss_points_list = gauss_points1(num_nodes_element, num_sides)

# Separa os pontos de Gauss em x e y
x = [point[0] for point in gauss_points_list]
y = [point[1] for point in gauss_points_list]

# Plota os pontos de Gauss
plt.scatter(x, y)
plt.title("Pontos de Gauss")
plt.xlabel("x")
plt.ylabel("y")
plt.show()