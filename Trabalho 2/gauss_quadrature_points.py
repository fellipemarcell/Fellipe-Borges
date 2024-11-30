import quadpy

def gauss_quadrature_points(n):
    # Criar um esquema de quadratura para um triângulo com n pontos
    scheme = quadpy.triangle.strang(n)
    
    # Obter os pontos e pesos
    points = scheme.points.T
    weights = scheme.weights
    
    return points, weights

# Exemplo de uso
n = 3  # Você pode alterar o valor de n para testar diferentes números de pontos
points, weights = gauss_quadrature_points(n)

print("Pontos:")
print(points)
print("Pesos:")
print(weights)