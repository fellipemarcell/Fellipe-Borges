
import numpy as np
from scipy.interpolate import griddata
import matplotlib.pyplot as plt

import calculate_exact_solution
from calculate_exact_solution import calculate_exact_solution
from plot_mesh import plot_mesh

def plot_numerical_contour(vertices, elements, u_numeric, u_exact, order):

    """
    Função para plotar as linhas de contorno da solução numérica e exata.

    Parâmetros
    ----------
        vertices : ndarray
            Coordenadas dos vértices da malha.
        elements : ndarray
            Matriz de conectividade dos elementos da malha.
        u_numeric : ndarray
            Solução numérica nos vértices.
        u_exact : ndarray
            Solução exata nos vértices.
        order : int
            Ordem dos polinômios de Lagrange usados ​​no cálculo.

    Retorna
    -------
        None
    """
    # # Verificar se os arrays de entrada são vazios
    # if not vertices or not elements or not u_numeric or not u_exact:
    #     raise ValueError("Vetores de entrada não podem ser vazios")

    # # Verificar se os arrays de entrada possuem dimensões corretas
    # if not isinstance(vertices, np.ndarray) or not isinstance(elements, np.ndarray) or not isinstance(u_numeric, np.ndarray) or not isinstance(u_exact, np.ndarray):
    #     raise TypeError("Vetores de entrada devem ser arrays numpy")

    # if vertices.ndim != 2 or elements.ndim != 2 or u_numeric.ndim != 1 or u_exact.ndim != 1:
    #     raise ValueError("Vetores de entrada devem ter dimensões correspondentes")

    # Extraindo as coordenadas de x e y
    x, y = zip(*vertices)

    # x = list(x)
    # y = list(y)

    # Criando uma grade regular para interpolar a solução
    # xi = np.linspace(x.min(), x.max(), 100)
    # yi = np.linspace(y.min(), y.max(), 100)
    xi = np.linspace(min(x), max(x), 100)
    yi = np.linspace(min(y), max(y), 100)
    xi, yi = np.meshgrid(xi, yi)

    # Interpolação dos valores de u_numeric na grade regular
    zi = griddata((x, y), u_numeric, (xi, yi), method = 'cubic')

    #Interpolação dos valores de u_exact na grade regular
    ze = griddata((x, y), calculate_exact_solution(100), (xi, yi), method = 'cubic')

    # Plotando as linhas de contorno
    plt.figure(figsize = (8, 6))
    contour = plt.contourf(xi, yi, zi, levels=20, cmap='viridis')
    plt.colorbar(contour, label='Solução numérica $u_{numeric}$')
    plt.xlabel('$x$')
    plt.ylabel('$y$')
    plt.title('Linhas de contorno da solução numérica $u_{numeric}$')
    plt.gca().set_aspect('equal')

    plt.figure(figsize = (8, 6))
    contour = plt.contourf(xi, yi, ze, levels=20, cmap='viridis')
    plt.colorbar(contour, label='Solução exata $u_{exact}$')
    plt.xlabel('$x$')
    plt.ylabel('$y$')
    plt.title('Linhas de contorno da solução exata $u_{exact}$')
    plt.gca().set_aspect('equal')
    plt.show()