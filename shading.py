from render.render_9627 import render
from render_object.util import render_object
from helpers import *
from lighting import *

import numpy as np


def calculate_normals(vertices, face_indices):
    num_faces = len(face_indices)
    num_vertices = len(vertices)
    normals = np.zeros((num_vertices, 3))

    for i in range(num_faces):
        current_face = face_indices[i]
        V0 = vertices[current_face[0]] 
        V1 = vertices[current_face[1]] 
        V2 = vertices[current_face[2]]
        E0 = V1 - V0
        E1 = V2 - V1
        # Each triangle a vertex is contained in contributes to the total normal.
        normals[current_face] += normalize(np.cross(E0, E1))
    for i in range(num_vertices):
        normals[i] = normalize(normals[i])
    return normals

