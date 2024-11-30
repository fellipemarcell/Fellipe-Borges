from matplotlib import pyplot as plt

def plot_convergence_comparison(h_values_dict, l2_errors_dict, energy_errors_dict):
    """
    Função para plotar a convergência da solução numérica para diferentes ordens de Lagrange.

    Recebe três dicionários:
    h_values_dict: dicionários com as chaves como as ordens dos polinômios de Lagrange e os valores como as listas com os tamanhos das malhas;
    l2_errors_dict: dicionários com as chaves como as ordens dos polinômios de Lagrange e os valores como as listas com os erros L2;
    energy_errors_dict: dicionários com as chaves como as ordens dos polinômios de Lagrange e os valores como as listas com os erros de Energia.

    Plota dois gráficos em uma janela:
    - O primeiro gráfico para o erro L2;
    - O segundo gráfico para o erro de Energia.
    """
    
    if not h_values_dict or not l2_errors_dict or not energy_errors_dict:
        raise ValueError("Os dicionários de entrada não podem ser vazios.")
    
    plt.figure(figsize=(12, 6))
    
    # Subplot para o erro L2
    plt.subplot(1, 2, 1)
    for order in h_values_dict.keys():
        if order not in l2_errors_dict:
            raise KeyError(f"Ordem {order} não encontrada em l2_errors_dict.")
        plt.loglog(h_values_dict[order], l2_errors_dict[order], label=f'Ordem {order}', marker='o')
    plt.xlabel('Tamanho da Malha (h)')
    plt.ylabel('Erro L2')
    plt.title('Convergência - Erro L2')
    plt.legend()
    plt.grid()
    
    # Subplot para o erro de energia
    plt.subplot(1, 2, 2)
    for order in h_values_dict.keys():
        if order not in energy_errors_dict:
            raise KeyError(f"Ordem {order} não encontrada em energy_errors_dict.")
        plt.loglog(h_values_dict[order], energy_errors_dict[order], label=f'Ordem {order}', marker='x')
    plt.xlabel('Tamanho da Malha (h)')
    plt.ylabel('Erro de Energia')
    plt.title('Convergência - Erro de Energia')
    plt.legend()
    plt.grid()

    # Ajustar espaçamento dos subplots
    plt.tight_layout()