import numpy as np
import assemble_system
from assemble_system import assemble_system
import apply_dirichlet
from apply_dirichlet import apply_dirichlet
import calculate_errors
from calculate_errors import calculate_errors
from calculate_polygon_vertices import calculate_polygon_vertices
from mesh import generate_mesh
import plot_convergence
from plot_convergence import plot_convergence
import plot_numerical_contour
from plot_numerical_contour import plot_numerical_contour
import solve_system
from solve_system import solve_system

def run_simulation(order, refinement_level, max_refinement_level, element_type, size):
    """
    Função para executar a simulação para uma ordem de Lagrange e nível de refinamento dados.

    Parameters
    ----------
    order : int
        Ordem do polinômio de Lagrange.
    refinement_level : int
        Nível de refinamento da malha.
    type_element : string
        Tipo de elemento (tri ou quad).

    Returns
    -------
    None

    """

    print(f"Executando simulação com elementos do tipo {element_type} com ordem: {order} e nível de refinamento: {refinement_level}")

    # Listas para armazenar os erros e tamanhos de malha
    l2_errors= []
    energy_errors =[]
    h_values =[]

    # Para o refinamento 1 até o máximo
    for refinement_level in range(1, max_refinement_level +1):

        #Gera a malha refinada
        nodes, elements = generate_mesh(size, refinement_level, element_type, order)

        # Vertices do elemento
        vertices = calculate_polygon_vertices(element_type)

        #Monta o sistema
        K, F = assemble_system(vertices, elements, order, element_type)
        K, F = apply_dirichlet(K, F, vertices)
        u_numeric = solve_system(K, F)
        #plot_solution(vertices, elements, u_numeric, order)

        #Solução exata
        u_exact= np.sin(np.pi * vertices[:,0]) * np.sin( np.pi * vertices[:,1])

        #Calcula erros
        l2_error, energy_error = calculate_errors(vertices, elements, u_numeric, u_exact, order)
        l2_errors.append(l2_error)
        energy_errors.append(energy_error)

        #Calcula o tamanho da malha e adiciona à lista
        h = np.sqrt(2)/refinement_level
        h_values.append(h)

        if refinement_level==max_refinement_level:
            #print(u_numeric)
            plot_numerical_contour(vertices, elements, u_numeric, u_exact, order)
            plot_convergence(h_values, l2_errors, energy_errors)

        print(f"Refinamento {refinement_level}: h = {h:.4f}, L2 Error = {l2_error:.4e}, Energy Error: {energy_error:.4e}")
