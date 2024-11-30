import numpy as np

def check_singularity(matrix):    
    """Verifica se a matriz de rigidez global é singular e aplica 'técnica de regularização' ou 'técnica de pre-condicionamento' para corrigir o problema.

    Parameters:
    matrix (scipy.sparse matrix): Matriz de rigidez do sistema.

    Returns:
    matrix (scipy.sparse matrix): Matriz de rigidez do sistema, corrigida caso seja singular.

    Raises:
    ValueError: Se a matriz de rigidez global for singular e as técnicas de corrigir o problema falharem.
    KeyError: Se a matriz de rigidez global for singular e as técnicas de corrigir o problema falharem.
    """
    # Obtem o tamanho da matriz
    n = matrix.shape[0]

    # Verifica se a matriz de rigidez global é singular
    try:
        if(np.linalg.matrix_rank(matrix.toarray()) < n):
            raise ValueError("Matriz de rigidez global é singular. Tentativa de 'regularização'.")
        matrix += 1e-6 * np.eye(n)
    except:
        pass
        
    try:
        if(np.linalg.matrix_rank(matrix.toarray()) < n):
            raise ValueError("Matriz de rigidez global é singular. Tentativa de aplicação de 'técnica de pre-condicionamento'.")
        matrix = preconditioner(matrix)
    except:
        pass    
        
    try:
        if(np.linalg.matrix_rank(matrix.toarray()) < n):
            raise ValueError("Matriz de rigidez global é singular. Provavelmente a matriz é singular por natureza.")
    except:
        return matrix
    
    return quit()

def preconditioner(K):
    """
    Preconditioner diagonal para o sistema linear.
    
    Parameters:
    K (scipy.sparse matrix): Matriz de rigidez do sistema.
    
    Returns:
    (numpy array): Inversa da diagonal da matriz de rigidez.
    """
    return np.linalg.inv(K.diagonal())
