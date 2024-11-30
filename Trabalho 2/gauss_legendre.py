import numpy as np

def gauss_legendre(n):
    """
    Calcula os coeficientes e pesos de Gauss-Legendre para uma ordem arbitrária.

    Parâmetros:
    n (int): Ordem do polinômio de Legendre.

    Retorno:
    x (numpy.array): Coeficientes de Gauss-Legendre.
    w (numpy.array): Pesos de Gauss-Legendre.
    """
    # Calcula os coeficientes de Legendre
    P = np.zeros((n+1, n+1))
    P[0, 0] = 1
    P[1, 0] = 0
    P[1, 1] = 1

    for i in range(2, n+1):
        P[i, 0] = 0
        for j in range(1, i+1):
            P[i, j] = ((2*i-1)*P[i-1, j-1] - (i-1)*P[i-2, j-1]) / i

    # Calcula os coeficientes de Gauss-Legendre
    x = np.zeros(n)
    w = np.zeros(n)

    for i in range(n):
        x[i] = np.roots(P[i, :])[0]
        if (1 - x[i]**2) == 0 or P[n, i]**2 == 0:
            w[i] = 0
        else:
            w[i] = (2 / (1 - x[i]**2)) / ((n+1)*P[n, i]**2)
    return x, w

n = 1  # Ordem do polinômio de Legendre
x, w = gauss_legendre(n)
print("Coeficientes de Gauss-Legendre:", x)
print("Pesos de Gauss-Legendre:", w)