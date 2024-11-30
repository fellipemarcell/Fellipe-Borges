import numpy as np
from numpy.polynomial.legendre import leggauss, legval

def gauss_legendre_coeffs_and_weights1(element_type, order):
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
    
    # Calcula os pontos de Gauss-Legendre e os pesos para a ordem especificada
    try:
        if element_type == "tri":
            points, weights = leggauss(order)
        elif element_type == "quad":
            points, weights = leggauss(order + 1)
    except Exception as e:
        raise RuntimeError(f"Erro ao calcular pontos e pesos de Gauss-Legendre: {e}")

    # Calcula os coeficientes de Gauss-Legendre
    coeffs = []
    for i in range(order + 1):
        try:
            coeffs.append(legval(points, np.poly1d([1] + [0]*i)))
        except Exception as e:
            raise RuntimeError(f"Erro ao calcular coeficientes de Gauss-Legendre: {e}")
    
    return np.array(coeffs), np.array(weights)

# element_type = "quad"
# order = 1
# coeffs, weights = gauss_legendre_coeffs_and_weights1(element_type, order)
# print(coeffs)
# print(weights)

element_type = "tri"
order = 2
coeffs, weights = gauss_legendre_coeffs_and_weights1(element_type, order)

print("Coeficientes:")
for i, coeff in enumerate(coeffs):
    print(f"Coeficiente {i+1}: {coeff}")

print("\nPesos:")
for i, weight in enumerate(weights):
    print(f"Peso {i+1}: {weight}")

# import pandas as pd

# element_type = "quad"
# order = 3
# coeffs, weights = gauss_legendre_coeffs_and_weights1(element_type, order)

# df = pd.DataFrame({
#     "Coeficiente": coeffs,
#     "Peso": weights
# })

# print(df)