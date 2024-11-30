import numpy as np
import apply_dirichlet
from apply_dirichlet import apply_dirichlet
import assemble_system
from assemble_system import assemble_system
import calculate_errors
from calculate_errors import calculate_errors
import calculate_exact_solution
from calculate_errors import calculate_errors
from calculate_exact_solution import calculate_exact_solution
from calculate_polygon_vertices import calculate_polygon_vertices
import check_singularity
from check_singularity import check_singularity
import compare_orders
from mesh import generate_mesh 
from mesh import plot_mesh
from mesh_size import calculate_mesh_size
import num_nodes_element
from num_nodes_element import num_nodes_element
import plot_convergence
from plot_convergence import plot_convergence
from plot_convergence_comparison import plot_convergence_comparison
import plot_numerical_contour
from plot_numerical_contour import plot_numerical_contour
import run_simulation
import solve_system
from solve_system import solve_system

size = 1.0  # Tamanho do domínio quadrado
refinement_level = 2  # Nível de refinamento da malha
element_type = 'tri' # Escolha do tipo de elemento: "tri" para triangular ou "quad" para quadrilátero
order = 3  # Ordem do polinômio de interpolação de Lagrange

# Gerar a malha usando Gmsh
nodes, elements = generate_mesh(size, refinement_level, element_type, order)

# Exibir os nós e elementos gerados
display = 'nodes' # Exibir malha ("mesh"), malha e nós ("nodes") ou malha e numeração dos nós ("val")

# Plotar a malha
plot_mesh(nodes, elements, display)

# Número de nós por elemento
nodes_element = num_nodes_element(element_type, order)
#print(nodes_element)

# Vertices do elemento
vertices = calculate_polygon_vertices(element_type)

# Montar o sistema FEM
K, F = assemble_system(vertices, elements, order, element_type)

# Verificar singularidade da matriz
K = check_singularity(K)

# Aplicar condições de contorno de Dirichlet 
K, F = apply_dirichlet(K, F, vertices)

# Verificar singularidade da matriz
K = check_singularity(K)

# Resolver o sistema linear
u_numeric = solve_system(K, F)

# Calcular a solução exata
u_exact = calculate_exact_solution(nodes)
# u_exact = np.zeros(len(nodes))
# for i, node in enumerate(nodes):
#     u_exact[i] = np.sin(np.pi * node[0]) * np.sin(np.pi * node[1])

# Calcular os erros
l2_error, energy_error = calculate_errors(vertices, elements, u_numeric, u_exact, order, element_type)

# Plotar a solução numérica
plot_numerical_contour(vertices, elements, u_numeric, u_exact, order)

# Calcular o tamanho dos elementos
areas = calculate_mesh_size(vertices, elements, element_type)

# Calcular o tamanho médio da malha (h)
plot_convergence(areas, l2_error, energy_error)

max_refinement_level = 10

# Definir os parâmetros de execução da simulação
run_simulation(order, refinement_level, max_refinement_level, element_type, size)

# Comparação de erros para diferentes ordens
h_values_dict, l2_errors_dict, energy_errors_dict = compare_orders(max_refinement_level, size, order, element_type)

# Comparação de desempenho
plot_convergence_comparison(h_values_dict, l2_errors_dict, energy_errors_dict)



# # Exibir os erros
# print("Erro L2:", l2_error)
# print("Erro de energia:", energy_error)

# # Exibir a solução numérica
# print("Solução numérica:")
# print(u_numeric)

# # Exibir a solução exata
# print("Solução exata:")
# print(u_exact)



# # Exibir os nós e elementos gerados
# print("Nós da malha:")
# print(nodes)
# print("Elementos da malha:")
# print(elements)

# # Função para determinar as funções de forma e gradientes
# num_total_nodes = nodes_element
# N, dN = shape_functions(num_total_nodes)



# print("Funções de forma:")
# for i, Ni in enumerate(N):
#     print(f"N{i} = {Ni}")

# print("\nGradientes:")
# for i, dNi in enumerate(dN):
#     print(f"dN{i} = {dNi}")