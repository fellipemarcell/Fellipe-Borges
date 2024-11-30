
import numpy as np
from sympy import lambdify, simplify, symbols

# Definição da função shape_functions
def shape_functions(num_total_nodes):
    """
    Calcula as funções de forma e gradientes dado um número total de nós
    
    Args:
    - num_total_nodes (int): Número total de nós.
    
    Returns:
    - N (list): Lista de funções de forma.
    - dN (list): Lista de gradientes das funções de forma.
    """
    if num_total_nodes <= 0:
        raise ValueError("O número total de nós deve ser maior que zero.")

    # Cria variáveis simbólicas
    x, y = symbols('x y')
    # Pontos de interpolação no polígono regular
    angles = np.linspace(0, 2 * np.pi, num_total_nodes, endpoint=False)
    xi = [(np.cos(angle), np.sin(angle)) for angle in angles]
    
    N = []  # Inicializa a lista de funções de forma
    dN = []  # Inicializa a lista de gradientes das funções de forma

    # Geração das funções de forma de Lagrange
    for i in range(num_total_nodes):
        Ni = 1  # Inicializa a função de forma Ni como 1
        for j in range(num_total_nodes):
            if i != j:
                denominator = (xi[i][0] - xi[j][0]) * (xi[i][1] - xi[j][1])
                if denominator == 0:
                    raise ZeroDivisionError("Divisão por zero ao calcular a função de forma.")

                # # Verifica se o denominador é muito próximo de zero
                # if np.isclose(denominator, 0):
                #     raise ZeroDivisionError("Divisão por um valor muito próximo de zero ao calcular a função de forma.")

                # Atualiza Ni multiplicando pelos termos de Lagrange
                Ni *= (x - xi[j][0]) * (y - xi[j][1]) / denominator
        Ni = simplify(Ni)  # Simplifica a expressão simbólica Ni
        N_lamb = lambdify((x, y), Ni)  # Converte a expressão simbólica Ni em uma função lambdificada para avaliação numérica
        dNi = [lambdify((x, y), Ni.diff(var)) for var in (x, y)]  # Calcula o gradiente de Ni com relação a x e y, e lambdifica essas derivadas
        N.append(N_lamb)  # Adiciona a função lambdificada Ni à lista de funções de forma
        dN.append(dNi)  # Adiciona os gradientes lambdificados dNi à lista de gradientes

    return N, dN  # Retorna as listas de funções de forma e gradientes

# Exemplo 1: Calcular as funções de forma e gradientes para um polígono regular com 3 nós
# num_total_nodes = 4
# N, dN = shape_functions(num_total_nodes)

# print("Funções de forma:")
# for i, Ni in enumerate(N):
#     print(f"N{i} = {Ni}")

# print("\nGradientes:")
# for i, dNi in enumerate(dN):
#     print(f"dN{i} = {dNi}")

# # Exemplo 2: Avaliar as funções de forma e gradientes em um ponto específico
# num_total_nodes = 4
# N, dN = shape_functions(num_total_nodes)

# # Defina um ponto (x, y) para avaliar as funções de forma e gradientes
# x, y = 0.5, 0.7

# print("Funções de forma avaliadas em (x, y) = ({}, {}):".format(x, y))
# for i, Ni in enumerate(N):
#     print(f"N{i}({x}, {y}) = {Ni(x, y)}")

# print("\nGradientes avaliados em (x, y) = ({}, {}):".format(x, y))
# for i, dNi in enumerate(dN):
#     print(f"dN{i}({x}, {y}) = {dNi[0](x, y)}, {dNi[1](x, y)}")

# # Exemplo 3: Plotar as funções de forma e gradientes
# import matplotlib.pyplot as plt
# import numpy as np

# num_total_nodes = 5
# N, dN = shape_functions(num_total_nodes)

# # Crie uma grade de pontos para plotar as funções de forma e gradientes
# x = np.linspace(-1, 1, 100)
# y = np.linspace(-1, 1, 100)
# X, Y = np.meshgrid(x, y)

# Plotar as funções de forma
# for i, Ni in enumerate(N):
#     Z = Ni(X, Y)
#     plt.contourf(X, Y, Z, cmap='viridis')
#     plt.title(f"Função de forma N{i}")
#     plt.show()

# # Plotar os gradientes
# for i, dNi in enumerate(dN):
#     dZ_dx = dNi[0](X, Y)
#     dZ_dy = dNi[1](X, Y)
#     plt.quiver(X, Y, dZ_dx, dZ_dy, color='blue')
#     plt.title(f"Gradiente dN{i}")
#     plt.show()