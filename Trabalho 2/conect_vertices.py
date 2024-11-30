from calculate_polygon_vertices import calculate_polygon_vertices

def conect_vertices(type_element):
    
    """
    Calcula as faces de um polígono regular conectando vértices consecutivos.

    Args:
    - type_element (str): Tipo de elemento: 'tri' para triângulo ou 'quad' para quadrilátero.

    Returns:
    - faces (list of lists): Lista de arestas, cada aresta conectando dois vértices consecutivos.
    """
    # Verifica se o tipo de elemento é válido
    if type_element is None:
        raise ValueError("Type element deve ser uma string.")
    if type_element not in ['tri', 'quad']:
        raise ValueError("Type element deve ser 'tri' ou 'quad'.")
    
    # Calcula o número de lados do polígono
    num_sides = 3 if type_element == 'tri' else 4  

    # Gera as faces conectando os vértices consecutivos
    faces = []
    for i in range(num_sides):
        face = [i, (i + 1) % num_sides]  # Conecta o vértice i com o vértice (i+1)
        faces.append(face)
    
    if len(faces) == 0:
        raise ValueError("Faces deve ser uma lista de listas.")
    
    return faces

# Exemplo de uso
type_element = 'quad'
vertices = calculate_polygon_vertices(type_element)
faces = conect_vertices(type_element)

#print("Vértices do polígono:", vertices)
print("Faces do polígono:", faces)