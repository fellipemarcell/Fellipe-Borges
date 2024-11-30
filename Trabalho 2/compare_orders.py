def compare_orders(max_refinement_level):
    #Dicionários para armazenar dados de erros e tamanhos de malhas
    h_values_dict = {}
    l2_errors_dict = {}
    energy_errors_dict = {}

    #Iterar sobre ordens
    for order in [1, 2, 3]:
        print(f"Executando para ordem {order}")

        l2_errors = []
        energy_errors =[]
        h_values = []

        #Executar simulação para níveis de refinamento
        for refinement_level in range(1, max_refinement_level):
            print(f"Refinamento nível {refinement_level}")

            #Geração da malha
            vertices, elements = generate_mesh(order, refinement_level)

            #Montar o sistema
            K, F = assemble_system(vertices, elements, order)
            K, F = apply_dirichlet(K, F, vertices)
            u_numeric = solve_system(K, F)

            #Solução exata
            u_exact = np.sin(np.pi * vertices[:,0]) * np.sin(np.pi * vertices[:,1])
            

            #calcula erros
            l2_error, energy_error = calculate_errors(vertices, elements, u_numeric, u_exact, order)
            l2_errors.append(l2_error)
            energy_errors.append(energy_error)

            #Calcular tamanho da malha
            h = np.sqrt(2)/refinement_level
            h_values.append(h)

            #Plotar solução na última iteração de refinamento
            if refinement_level == max_refinement_level:
                print(f" Plotando solução para ordem P{order} no refinamento{refinement_level}")
                plot_solution(vertices, elements, u_numeric, u_exact, order)

        #Armazenar resultados para cada ordem
        h_values_dict[order] = h_values
        l2_errors_dict[order] = l2_errors
        energy_errors_dict[order] = energy_errors

    #Plotar comparação de erros
    plot_convergence_comparison(h_values_dict, l2_errors_dict, energy_errors_dict)
    plt.show()