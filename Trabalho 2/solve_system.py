import scipy.sparse.linalg as spla
import numpy as np
import scipy.linalg as lil
import scipy.sparse as dok

#Função para resolver o sistema
def solve_system(K, F):
    """
    Resolve o sistema linear Ku = F, onde K é uma matriz esparsa e F é um vetor.

    Parâmetros:
    K (scipy.sparse matrix): Matriz de rigidez do sistema.
    F (numpy array): Vetor de for a do sistema.

    Retorna:
    u (numpy array): Vetor de deslocamento do sistema.

    Exce es:
    ValueError: se K ou F forem nulos.
    TypeError: se K ou F tiverem tipos errados.
    """
    if K is None or F is None:
        raise ValueError("K e F não podem ser nulos")
    # if not isinstance(K, (spla.csc_matrix, spla.csr_matrix)):
    #     raise TypeError("K deve ser uma matriz esparsa")
    if not isinstance(F, np.ndarray):
        raise TypeError("F deve ser um vetor numpy")
    
    # u = lil.solve(K, F)
    u = spla.spsolve(K,F)
    # u = dok.solve(K, F)
    return u
