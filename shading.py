from logging import exception
from render.render_9627 import *
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
    verts_3d, verts_p, verts_n, verts_c, b_coords, cam_pos,
    ka, kd, ks, n, light_positions, light_intensities, Ia, X, M, N
):
    I = np.zeros((3, 3)) # 3 colors for each one of the 3 vertices.
    for i in range(3):
        I[i] = total_lighting(
            verts_3d[i], verts_n[i], verts_c[i], cam_pos, ka, kd, ks, n, light_positions, light_intensities, Ia
        )
        X[verts_p[i, 0]][verts_p[i, 1]] *= I[i]
        verts_c[i] *= I[i]
    X = shade_triangle(X, verts_p, verts_c, "gouraud", M, N)

    return X



def shade_phong(
    verts_p, verts_n, verts_c, b_coords, cam_pos, ka, kd, ks, n,
    light_position, light_intensities, Ia, X
):
    pass


def render_object(
    shader, focal, eye, lookat, up, bg_color, M, N, H, W, verts, vert_colors,
    face_indices, ka, kd, ks, n, light_position, light_intensities, Ia
):
    img = initialize_img(M, N, bg_color)
    normals = calculate_normals(verts, face_indices)
    verts2d, depths = project_cam_lookat(focal, eye, lookat, up, verts)
    verts_rast, __, __ = rasterize(verts2d, M, N, H, W)
    verts_rast = verts_rast.astype(int)
    keep_faces = get_keep_indices(face_indices, verts_rast, M, N)

    num_faces = len(keep_faces)
    b_coords = np.zeros((num_faces, 2))
    img = color_vertices(img, vert_colors, verts_rast, keep_faces)

    if shader == "gouraud":
        for i in range(num_faces):
            face = keep_faces[i]
            b_coords[i] = find_barycenter(verts_rast[face])
            img = shade_gouraud(
                verts[face], verts_rast[face], normals[face], vert_colors[face], b_coords[i],
                eye, ka, kd, ks, n, light_position, light_intensities, Ia, img, M, N
            )
        cv.imshow("img", img)
        cv.waitKey(0)
        cv.destroyAllWindows()
    elif shader == "phong":
        pass
    else:
        exit("`shader` can only be \"gouraud\" or \"phong\".")