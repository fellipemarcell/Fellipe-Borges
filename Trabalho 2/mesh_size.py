import numpy as np


def calculate_mesh_size(vertices, elements, type_element):
    """
    Calcula o tamanho médio da malha (h) a partir de suas vértices e elementos.

    Parameters
    ----------
    vertices : ndarray
        Array de vértices da malha.
    elements : ndarray
        Array de elementos da malha.

    Returns
    -------
    float
        Tamanho médio da malha (h).
    """
    areas = []
    if type_element == "tri":
        for elem in elements:
            node_coords = vertices[elem]
            area=0.5 * abs(np.linalg.det(np.array([[1, node_coords[0][0], node_coords[0][1]],
                                                  [1, node_coords[1][0], node_coords[1][1]],
                                                  [1, node_coords[2][0], node_coords[2][1]]])))
            areas.append(area)
    elif type_element == "quad":
        for elem in elements:
            node_coords = vertices[elem]
            area=0.5 * abs(np.linalg.det(np.array([[1, node_coords[0][0], node_coords[0][1]],
                                                  [1, node_coords[1][0], node_coords[1][1]],
                                                  [1, node_coords[2][0], node_coords[2][1]],
                                                  [1, node_coords[3][0], node_coords[3][1]]])))
        areas.append(area)

    return np.mean(areas)