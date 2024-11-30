def plot_convergence(h_values, l2_errors, energy_errors):
    plt.figure()
    plt.loglog(h_values, l2_errors, label='Erro L2', marker='o')
    plt.loglog(h_values, energy_errors, label='Erro de Energia', marker='x')
    plt.xlabel('Tamanho da Malha (h)')
    plt.ylabel('Erro')
    plt.title('Análise de convergência')
    plt.legend()
    plt.grid()
