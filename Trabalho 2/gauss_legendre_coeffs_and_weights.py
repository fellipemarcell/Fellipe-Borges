import numpy as np
from numpy.polynomial.legendre import leggauss

def gauss_legendre_coeffs_and_weights(element_type, order):
    """
    Calcula os coeficientes e pesos de Gauss-Legendre para um número de pontos específico.

    Args:
    - element_type (str): 'tri' para triângulo ou 'quad' para quadrilátero'.
    - order (int): A ordem da quadratura de Gauss.

    Returns:
    - coeffs (numpy.ndarray): Os coeficientes de Gauss-Legendre.
    - weights (numpy.ndarray): Os pesos de Gauss-Legendre.
    """
    # Verifica se o tipo de elemento é válido    
    if not isinstance(element_type, str) or element_type is None:
        raise ValueError('O tipo de elemento deve ser uma string não nula.')
    if element_type not in ['tri', 'quad']:
        raise ValueError("O elemento deve ser triângulo ou quadrilátero. Use 'tri' or 'quad'.")

    # Verifica se a ordem do polinômio é inteiro e maior que zero
    if not isinstance(order, int) or order is None:
        raise ValueError('A ordem deve ser um inteiro não nulo.')
    if order < 1:
        raise ValueError('A ordem deve ser positiva.')

    # Calcula o número de nós no interior e nas arestas do elemento
    if element_type == "tri":
        num_sides = 3
    elif element_type == "quad":
        num_sides = 4
    
    # Calcula o número total de nós
    num_edge_nodes = order - 1  # Nós adicionais por aresta
    num_points = (num_sides * (num_edge_nodes + 1)) + (order - 1) * (order - 2) // 2  # Total de nós (vértices + nós interiores)
    
    # Verifica se o número de pontos é maior que zero
    if num_points <= 0:
        raise ValueError('O número total de pontos deve ser maior que zero.')
    
    # Calcula os coeficientes e pesos
    coeffs = np.polynomial.legendre.legroots(num_points)
    weights = 2 / ((1 - coeffs**2) * (num_points - 1)**2)
    
    return coeffs, weights

# # Exemplo
# element_type = "quad"
# order = 3
# coeffs, weights = gauss_legendre_coeffs_and_weights(element_type, order)
# print(coeffs)
# print(weights)

element_type = "tri"
order = 3
coeffs, weights = gauss_legendre_coeffs_and_weights(element_type, order)

print("Coeficientes:")
for i, coeff in enumerate(coeffs):
    print(f"Coeficiente {i+1}: {coeff}")

print("\nPesos:")
for i, weight in enumerate(weights):
    print(f"Peso {i+1}: {weight}")