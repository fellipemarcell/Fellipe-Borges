import numpy as np
import scipy as sp
from scipy.sparse import lil_matrix
from calculate_polygon_vertices import calculate_polygon_vertices
from gauss_quadrature_points2 import gauss_quadrature_points2
from shape_functions import shape_functions
from numpy.linalg import matrix_rank

# Função para montar o sistema FEM
def assemble_system(vertices, elements, order, type_element):
    """
    Monta o sistema FEM para um problema de equação de Poisson.

    Entrada:
    - vertices (array): Coordenadas dos vértices da malha.
    - elements (lista de array): Conectividade da malha onde cada entrada lista os índices de vértices de um elemento.
    - order (int): A ordem polinomial para as funções de forma.
    - type_element (str): O tipo de elemento: 'tri' para triângulo ou 'quad' para quadrilátero.

    Saída:
    - tupla: Uma tupla contendo:
        - K (scipy.sparse.csc_matrix): A matriz de rigidez global montada em formato de coluna esparsa compactada.
        - F (numpy.ndarray): O vetor de força global montado.
    """
    # Verifica se as entradas são vazias
    if vertices is None or elements is None:
        raise ValueError("Matriz K, vetor F, ou vértices não podem ser vazios")
    
    # # Verifica se as entradas são matrizes e vetores numpy
    # if not isinstance(vertices, np.ndarray) or not isinstance(elements, list):
    #     raise TypeError("Matriz K e vetor F devem ser matrizes e vetores numpy")
    
    # # Verifica se as entradas possuem as dimensões corretas
    # if len(vertices.shape) != 2 or len(elements) == 0:
    #     raise ValueError("Matriz K e vetor F devem ter dimensões 2 e 1, respectivamente")

    # Verifica se os elementos da malha são triângulos ou quadriláteros
    if type_element not in ['tri', 'quad']:
        raise ValueError("Tipo de elemento inválido. Deve ser 'tri' ou 'quad'")
    
    # Número de nós
    num_nodes = len(vertices)

    # Inicializa a matriz de rigidez e o vetor de força
    K_global = lil_matrix((num_nodes, num_nodes))
    F_global = np.zeros(num_nodes)

    # Função de fonte
    source_function = lambda x, y: 2 * np.pi**2 * np.sin(np.pi * x) * np.sin(np.pi * y) 

    # Calcula os pontos de Gauss e seus pesos para o triângulo ou quadrilátero
    gauss_points = gauss_quadrature_points2(type_element, order)
    
    # Calcula as funções de forma e seus gradientes
    shape_funcs, grad_shape_funcs = shape_functions(order)

    # Itera sobre os elementos
    for element in elements:
        node_indices = element
        node_coords = vertices[node_indices]
        num_element_nodes = len(node_indices)

        # Inicializa a matriz de rigidez e o vetor de força do elemento
        K_element = np.zeros((num_element_nodes, num_element_nodes))
        F_element = np.zeros(num_element_nodes)

        # Itera sobre os pontos de Gauss
        for (xi, yi, weight) in gauss_points:
            x_gauss = sum(node_coords[i][0] * shape_funcs[i](xi, yi) for i in range(num_element_nodes))
            y_gauss = sum(node_coords[i][1] * shape_funcs[i](xi, yi) for i in range(num_element_nodes))

            # Calcula o Jacobiano
            J = np.array([
                [sum(node_coords[i][0] * grad_shape_funcs[i][0](xi, yi) for i in range(num_element_nodes)),
                 sum(node_coords[i][0] * grad_shape_funcs[i][1](xi, yi) for i in range(num_element_nodes))],
                [sum(node_coords[i][1] * grad_shape_funcs[i][0](xi, yi) for i in range(num_element_nodes)),
                 sum(node_coords[i][1] * grad_shape_funcs[i][1](xi, yi) for i in range(num_element_nodes))]
            ])

            # Calcula o determinante do Jacobiano
            detJ = np.linalg.det(J)
            if detJ == 0:
                raise ValueError("Verificando se o determinante do Jacobiano é zero (configuração singular).")
            
            # Calcula a inversa do Jacobiano
            invJ = np.linalg.inv(J)

            # Calcula a área do elemento
            if type_element == 'tri':
                element_area = 0.5 * abs(detJ)
            elif type_element == 'quad':
                element_area = abs(detJ)
            else:
                raise ValueError("Tipo de elemento desconhecido.")
            
            # Itera sobre as funções de forma
            for i in range(num_element_nodes):
                for j in range(num_element_nodes):
                    grad_Ni = invJ.T @ np.array([grad_shape_funcs[i][0](xi, yi), grad_shape_funcs[i][1](xi, yi)])
                    grad_Nj = invJ.T @ np.array([grad_shape_funcs[j][0](xi, yi), grad_shape_funcs[j][1](xi, yi)])
                    K_element[i, j] += (grad_Ni @ grad_Nj) * element_area * weight
                F_element[i] += source_function(x_gauss, y_gauss) * shape_funcs[i](xi, yi) * element_area * weight

        # Adiciona a matriz de rigidez e o vetor de força ao sistema global
        for i in range(num_element_nodes):
            for j in range(num_element_nodes):
                K_global[node_indices[i], node_indices[j]] += K_element[i, j]
            F_global[node_indices[i]] += F_element[i]
        
        # Verifica se a matriz de rigidez global é esparsa
        if K_global.getnnz() == 0:
            raise ValueError("Matriz de rigidez global é esparsa.")
        
        n = K_global.shape[0]

        # Verifica se a matriz de rigidez global é singular
        try:
            if(np.linalg.matrix_rank(K_global.toarray()) < n):
                raise ValueError("Matriz de rigidez global é singular. Tentativa de 'regularização'.")
            K_global += 1e-6 * np.eye(n)
        except:
            pass
        
        try:
            if(np.linalg.matrix_rank(K_global.toarray()) < n):
                raise ValueError("Matriz de rigidez global é singular. Tentativa de aplicação de 'técnica de pre-condicionamento'.")
            K_global = preconditioner(K_global)
        except:
            pass    
        
        try:
            if(np.linalg.matrix_rank(K_global.toarray()) < n):
                raise ValueError("Matriz de rigidez global é singular. Provavelmente a matriz é singular por natureza.")
        except:
            pass
    
    return K_global.tocsc(), F_global

def preconditioner(K):
    """
    Preconditioner diagonal para o sistema linear.
    
    Parameters:
    K (scipy.sparse matrix): Matriz de rigidez do sistema.
    
    Returns:
    (numpy array): Inversa da diagonal da matriz de rigidez.
    """
    return np.linalg.inv(K.diagonal())

# # Exemplo de uso
# type_element = 'quad'  # Tipo de elemento: 'tri' para triângulo ou 'quad' para quadrilátero
# order = 1  # Grau do polinômio

# vertices = calculate_polygon_vertices(type_element)  # Calcula os vértices do polígono
# elements = 

# K, F = assemble_system(vertices, elements, order, type_element)
# print("Matriz de Rigidez K:\n", K.toarray())
# print("Vetor de Força F:\n", F)