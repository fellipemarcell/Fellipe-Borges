import numpy as np
from numpy.polynomial.legendre import leggauss
import matplotlib.pyplot as plt

def gauss_quadrature_points2(type_element, order):
    """
    Retorna os pontos de Gauss e os pesos para um polígono regular de acordo com o número de lados e a ordem especificados.

    Args:
    - type_element('string'): O tipo de elemento: 'tri' para triângulo ou 'quad' para quadrilátero.
    - order (int): A ordem da quadratura de Gauss.

    Returns:
    - points (list of tuples): Lista de tuplas contendo os pontos de Gauss e o pesos correspondentes (xi, yi, weigthi) no polígono.

    Raises:
    - ValueError: Se o número de lados for inválido.
    """
    # Verifica se o número de lados do polígono regular é um inteiro positivo
    if type_element == 'tri':
        gauss_points = gauss_quadrature_points_triangle(order)
    elif type_element == 'quad':
        gauss_points = gauss_quadrature_points_square(order)
    else:
        raise ValueError("O elemento deve ser triângulo ('tri') ou quadrilátero ('quad').")

    return gauss_points
    
def gauss_quadrature_points_triangle(n):
    """
    Retorna os pontos de Gauss e os pesos para um triângulo de acordo com a ordem especificada.

    Args:
    - n (int): A ordem da quadratura de Gauss.

    Returns:
    - points (list of tuples): Lista de tuplas contendo os pontos de Gauss e os pesos correspondentes (xi, yi, weigthi) no triângulo.

    Raises:
    - ValueError: Se o número de pontos for inválido.
    """
    # Verifica se o número de pontos em cada lado do triângulo é um inteiro positivo
    if not isinstance(n, int) or n < 1:
        raise ValueError('O número de pontos em cada lado do triângulo deve ser um inteiro positivo.')
    
    # Define os pontos de Gauss e seus pesos para o triângulo
    if n == 1:
        gauss_points = [(1/3, 1/3, 1/2)]
    elif n == 3:
        gauss_points = [(1/2, 0, 1/6), (0, 1/2, 1/6), (1/2, 1/2, 1/6)]
    elif n == 4:
        gauss_points = [(1/3, 1/3, -27/96), (0.6, 0.2, 25/96), (0.2, 0.6, 25/96), (0.2, 0.2, 25/96)]
    elif n == 6:
        a = 0.816847572980459
        b = 0.091576213509771
        w1 = 0.109951743655322
        w2 = 0.223381589678011
        gauss_points = [(a, b, w1), (b, a, w1), (b, b, w1), (1/2, 1/2, w2), (1/2, 0, w2), (0, 1/2, w2)]
    elif n==10:
        a = 333333/1000000
        b = 489682/1000000
        c = 21636/1000000
        d = 437089/1000000
        e = 125822/1000000
        f = 188203/1000000
        g = 623594/1000000
        w1 = 9/80
        w2 = 66197/1000000
        w3 = 62969/1000000
        w4 = 34229/1000000
        gauss_points = [(a, a, w1), (b, b, w2), (b, c, w2), (c, b, w3), (d, d, w3), (d, e, w3), (e,d, w3), (f, f, w4), (f, g, w4), (g, f, w4)]
    else:
        raise ValueError("Número de pontos não suportado para triângulo")
    
    # Verifica se a lista de pontos de Gauss foi criada corretamente
    if not isinstance(gauss_points, list):
        raise ValueError("A lista de pontos de Gauss não é uma lista")
    if len(gauss_points) != n:
        raise ValueError("A lista de pontos de Gauss tem tamanho diferente do especificado")
    for point in gauss_points:
        if not isinstance(point, tuple) or len(point) != 3:
            raise ValueError("Um dos pontos de Gauss não é uma tupla com 3 elementos")
        if not (isinstance(point[0], (int, float)) and isinstance(point[1], (int, float)) and isinstance(point[2], (int, float))):
            raise ValueError("Um dos pontos de Gauss tem elemento que não é um número")

def gauss_quadrature_points_square(n):
    """
    Retorna uma lista de tuplas com os pontos de Gauss e respectivos pesos
    para um quadrado com n pontos em cada lado.

    Parâmetros:
    - n (int): Número de pontos em cada lado do quadrado.

    Retorna:
    - gauss_points (list of tuples): Lista de tuplas contendo os pontos de Gauss (xi, yi, weighti) e os respectivos pesos.
    
    Raises:
    - ValueError: Se n for menor que 1.
    - RuntimeError: Se houver um erro ao calcular os pontos e pesos de Gauss-Legendre.
    """
    # Verifica se o número de pontos em cada lado do quadrado é um inteiro positivo
    if not isinstance(n, int) or n < 1:
        raise ValueError('O número de pontos em cada lado do quadrado deve ser um inteiro positivo.')
    
    # Define os pontos de Gauss e seus pesos para o quadrado
    try:
        points, weights = leggauss(n)
        if points is None or weights is None:
            raise RuntimeError("Erro ao calcular pontos e pesos de Gauss-Legendre: retornou None")
        if not isinstance(points, list) or not isinstance(weights, list):
            raise RuntimeError("Erro ao calcular pontos e pesos de Gauss-Legendre: retornou tipo inválido")
        if len(points) != n or len(weights) != n:
            raise RuntimeError("Erro ao calcular pontos e pesos de Gauss-Legendre: tamanho diferente do especificado")
        if any(p is None or w is None for p, w in zip(points, weights)):
            raise RuntimeError("Erro ao calcular pontos e pesos de Gauss-Legendre: vazio")
    except Exception as e:
        raise RuntimeError(f"Erro ao calcular pontos e pesos de Gauss-Legendre: {e}")

    # Inicializa a lista de pontos de Gauss
    gauss_points = [] 

    # Calcula os pontos de Gauss
    for i in range(n):
        for j in range(n):
            xi = points[i]
            eta = points[j]
            weight = weights[i] * weights[j]
            gauss_points.append((xi, eta, weight))
    
    return gauss_points

def plot_gauss_points(gauss_points, element_type):
    """
    Plota os pontos de Gauss e os seus pesos em um gráfico de dispersão.

    Args:
    - gauss_points (list of tuples): Lista de tuplas contendo os pontos de Gauss (xi, yi) e os pesos correspondentes.
    - element_type (str): O tipo de elemento, utilizado para o título do gráfico, por exemplo, 'tri' para triângulo.

    O gráfico apresenta pontos de Gauss coloridos de acordo com seus pesos, com uma barra de cores indicando o valor do peso.
    """
    # Verifica se os argumentos são válidos
    if not isinstance(gauss_points, list) or len(gauss_points) == 0:
        raise ValueError("Lista de pontos de Gauss vazia")
    if not isinstance(element_type, str) or len(element_type) == 0:
        raise ValueError("O tipo de elemento deve ser uma string não vazia")

    # Extrai os pontos de Gauss e seus pesos
    x = [point[0] for point in gauss_points]
    y = [point[1] for point in gauss_points]
    weights = [point[2] for point in gauss_points]

    # Verifica se os pesos são números inteiros ou decimais positivos
    if not all(isinstance(w, (int, float)) and w >= 0 for w in weights):
        raise ValueError("Os pesos devem ser números inteiros ou decimais positivos")
    
    # Plota os pontos de Gauss e seus pesos
    try:
        plt.scatter(x, y, c=weights, cmap='viridis', marker='o')
        plt.colorbar(label='Pesos')
        plt.xlabel('ξ')
        plt.ylabel('η')
        plt.title(f'Pontos de Gauss e Pesos para {element_type}')
        plt.grid(True)
        plt.show()
    except Exception as e:
        raise RuntimeError(f"Erro ao plotar pontos de Gauss: {e}")

# Exemplo de uso para triângulos
# type_element = 'tri'
# order = 10 
# gauss_point = gauss_quadrature_points2(type_element, order)

# print(gauss_point)

# print("Triângulo - Pontos e Pesos:")
# for p in gauss_point:
#     print(f"({p[0]}, {p[1]}) - Peso: {p[2]}")

# plot_gauss_points(gauss_point, 'tri')

# # Exemplo de uso para quadrados
# type_element = 'quad'
# order = 2
# gauss_point = gauss_quadrature_points2(type_element, order)
# 
# print(gauss_point)
# 
# print("Quadrado - Pontos e Pesos:")
# for p in gauss_point:
#     print(f"({p[0]}, {p[1]}) - Peso: {p[2]}")

# plot_gauss_points(gauss_points, 'quad')