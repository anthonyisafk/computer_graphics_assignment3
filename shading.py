from logging import exception
from render.render_9627 import render
from render_object.util import *
from helpers import *
from lighting import *

import numpy as np
import cv2 as cv


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
        E1 = V2 - V0
        # Each triangle a vertex is contained in contributes to the total normal.
        normals[current_face] += normalize(np.cross(E0, E1))
    for i in range(num_vertices):
        normals[i] = normalize(normals[i])
    return normals


def shade_gouraud(
    verts_p, verts_n, verts_c, b_coords, cam_pos, ka, kd, ks, n,
    light_positions, light_intensities, Ia, X
):
    pass


def  shade_phong(
    verts_p, verts_n, verts_c, b_coords, cam_pos, ka, kd, ks, n,
    light_position, light_intensities, Ia, X
):
    pass



def render_object(
    shader, focal, eye, lookat, up, bg_color, M, N, H, W, verts, vert_colors,
    face_indices, ka, kd, ks, n, light_position, light_intensities, Ia
):
    num_faces = len(face_indices)
    normals = calculate_normals(verts, face_indices)
    verts2d, depths = project_cam_lookat(focal, eye, lookat, up, verts)
    verts_rast, __, __ = rasterize(verts2d, M, N, H, W)
    keep_faces = get_keep_indices(face_indices, verts_rast, M, N)

    if shader == "gouraud":
        pass
    elif shader == "phong":
        pass
    else:
        exit("`shader` can only be \"gouraud\" or \"phong\".")