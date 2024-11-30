import numpy as np
import gauss_points
from gauss_quadrature_points2 import gauss_quadrature_points2
import shape_functions
from shape_functions import shape_functions

def calculate_errors(vertices, elements, u_numeric, u_exact, order, element_type):
    """
    Calcular erros L2 e de energia entre as soluções numéricas e exatas.

    Parâmetros
    ----------
        vértices : ndarray
        Coordenadas dos vértices da malha.
        elementos : ndarray
        Matriz de conectividade dos elementos da malha.
        u_numeric : ndarray
        Solução numérica nos vértices.
        u_exact : ndarray
        Solução exata nos vértices.
        order : int
        Ordem dos polinômios de Lagrange usados ​​no cálculo.

    Retorna
    -------
        l2_error : float
        Erro L2 entre as soluções numéricas e exatas.
        energy_error : float
        Erro de energia entre as soluções numéricas e exatas.
    """
    
    # Verificar se os arrays de entrada são vazios
    # if not vertices or not elements or not u_numeric or not u_exact:
    #     raise ValueError("Input arrays cannot be empty")
    
    # Verificar se os arrays de entrada possuem dimensões corretas
    # if not isinstance(vertices, np.ndarray) or not isinstance(elements, np.ndarray) or not isinstance(u_numeric, np.ndarray) or not isinstance(u_exact, np.ndarray):
    #     raise TypeError("Input arrays must be numpy arrays")
    
    # if vertices.ndim != 2 or elements.ndim != 2 or u_numeric.ndim != 1 or u_exact.ndim != 1:
    #     raise ValueError("Input arrays must have 2 dimensions and 1 dimension respectively")
    
    # Inicializar os erros
    l2_error = 0
    energy_error = 0

    # Calcular os pontos de Gauss
    gauss_points = gauss_quadrature_points2(element_type, order)

    # Calcular as funções de forma
    N, dN = shape_functions(order)

    try:
        # Calcular os erros para cada elemento
        for elem in elements:
            node_indices = elem
            node_coords = vertices[node_indices]

            # Calcular os erros para cada ponto de Gauss
            u_exact_vals = u_exact[node_indices]
            u_numeric_vals = u_numeric[node_indices]

            # Calcular os erros
            for (xi, yi, weight) in gauss_points:
                x_gauss = sum(node_coords[i][0] * N[i](xi, yi) for i in range(len(node_indices)))
                y_gauss = sum(node_coords[i][1] * N[i](xi, yi) for i in range(len(node_indices)))

                # Calcular o Jacobiano
                J = np.array([
                    [sum(node_coords[i][0] * dN[i](xi, yi)[0] for i in range(len(node_indices))),
                     sum(node_coords[i][0] * dN[i](xi, yi)[1] for i in range(len(node_indices)))],
                    [sum(node_coords[i][1] * dN[i](xi, yi)[0] for i in range(len(node_indices))),
                     sum(node_coords[i][1] * dN[i](xi, yi)[1] for i in range(len(node_indices)))]                    ])

                # Calcular o determinante e a inversa do Jacobiano
                detJ = np.linalg.det(J)
                if detJ == 0:
                    raise ValueError("O determinante jacobiano é zero, verifique os vértices de entrada para colinearidade")
                invJ = np.linalg.inv(J)

                # Calcular a área
                if type == "tri":
                    area = 0.5 * abs(detJ)
                elif type == "quad":
                    area = abs(detJ)
                else:
                    raise ValueError("Tipo de elemento desconhecido")

                # Soluções exata e numérica
                u_exact_gauss = np.sin(np.pi * x_gauss) * np.sin(np.pi * y_gauss)
                u_numeric_gauss = sum(u_numeric_vals[i] * N[i](xi, yi) for i in range(len(node_indices)))

                # Calcular os erros L2
                l2_error += ((u_exact_gauss - u_numeric_gauss) ** 2) * area * weight

                # Calcular o gradiente exato
                grad_u_exact = np.array([
                    np.pi * np.cos(np.pi * x_gauss) * np.sin(np.pi * y_gauss),
                    np.pi * np.sin(np.pi * x_gauss) * np.cos(np.pi * y_gauss)
                ])

                # Calcular o gradiente numérico
                grad_u_numeric = np.zeros(2)
                for i in range(len(node_indices)):
                    grad_Ni = invJ.T @ dN[i](xi, yi)
                    grad_u_numeric += u_numeric_vals[i] * grad_Ni

                # Calcular o erro de energia
                energy_error += (np.linalg.norm(grad_u_exact - grad_u_numeric) ** 2) * area * weight

        return np.sqrt(l2_error), np.sqrt(energy_error)

    except Exception as e:
        raise RuntimeError("Erro no cálculo de erros: {}".format(str(e)))
