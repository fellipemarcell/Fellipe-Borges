import numpy as np
def calculate_polygon_vertices(type_element, radius=1):
    """
    Calcula os vértices de um triângulo ou quadrilátero.
    
    Args:
    - type_element (str): 'tri' para triângulo ou 'quad' para quadrilátero.
    - radius (float): Raio do elemento.
    
    Returns:
    - vertices (list of tuples): Lista de vértices do elemento.
    
    Raises:
    - ValueError: Se o tipo de elemento for inválido.
    - ValueError: Se o raio for menor ou igual a zero.
    """
    # Verifica se o tipo de elemento é valido
    if not isinstance(type_element, str) or type_element is None:
        raise ValueError("O tipo de elemento deve ser uma string não vazia")
    
    if type_element not in ['tri', 'quad']:
        raise ValueError("O elemento deve ser triângulo ('tri') ou quadrilátero ('quad').")
    
    if radius <= 0:
        raise ValueError("O raio deve ser inteiro e positivo")
    
    num_sides = 3 if type_element == 'tri' else 4 
    
    # Calcula o angulo central
    central_angle = 2 * np.pi / num_sides
    
    # Gera os vértices do polígono
    vertices = []
    for i in range(num_sides):
        angle = i * central_angle
        x = radius * np.cos(angle)
        y = radius * np.sin(angle)
        vertices.append((x, y))
    
    return vertices

# Exemplo de uso
# type_element = 'tri'  # Tipo de elemento: 'tri' para triângulo ou 'quad' para quadrilátero
# radius = 1  # Raio do polígono
# vertices = calculate_polygon_vertices(type_element, radius)
# print("Vértices do polígono:", vertices)

# print('Teste:')
# x, y = zip(*vertices)
# print(x, y)