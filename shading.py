from render.render_9627 import *
from render_object.util import *
from helpers import *
from lighting import *
from phong import *

import numpy as np
import cv2 as cv


def render_object(
    shader, focal, eye, lookat, up, bg_color, M, N, H, W, verts, vert_colors,
    face_indices, ka, kd, ks, n, light_position, light_intensities, Ia
):
    img = initialize_img(N, M, bg_color)
    normals = calculate_normals(verts, face_indices)
    verts2d, depths = project_cam_lookat(focal, eye, lookat, up, verts)
    verts_rast, __, __ = rasterize(verts2d, N, M, H, W)
    verts_rast = verts_rast.astype(int)

    keep_faces = get_keep_indices(face_indices, verts_rast, N, M)
    triangle_depths, idx = calculate_useful_depths(keep_faces, depths)

    num_faces = len(keep_faces)
    b_coords = np.zeros((num_faces, 3))
    for i in range(num_faces):
        b_coords[i] = find_barycenter(verts[keep_faces[i]])

    if shader == "gouraud":
        for i in range(num_faces):
            face = keep_faces[idx[i]]
            img = shade_gouraud(
                verts_rast[face], normals[face], vert_colors[face], b_coords[idx[i]],
                eye, ka, kd, ks, n, light_position, light_intensities, Ia, img, N, M
            )
    elif shader == "phong":
        for i in range(num_faces):
            face = keep_faces[idx[i]]
            img = shade_phong(
                verts_rast[face], normals[face], vert_colors[face], b_coords[idx[i]],
                eye, ka, kd, ks, n, light_position, light_intensities, Ia, img, N, M
            )
    else:
        exit("`shader` can only be \"gouraud\" or \"phong\".")

    return img


def shade_gouraud(
    verts_p, verts_n, verts_c, b_coords, cam_pos,
    ka, kd, ks, n, light_positions, light_intensities, Ia, X, M, N
):
    I = np.zeros(3)
    for i in range(3):
        I = total_lighting(
            b_coords, verts_n[i], verts_c[i], cam_pos, ka, kd, ks, n, light_positions, light_intensities, Ia
        )
        X[verts_p[i, 0]][verts_p[i, 1]] = I
        verts_c[i] = I
    X = shade_triangle(X, verts_p, verts_c, "gouraud", N, M)
    return X


def shade_phong(
    verts_p, verts_n, verts_c, b_coords, cam_pos,
    ka, kd, ks, n, light_positions, light_intensities, Ia, X, M, N
):
    n = len(verts_p)
    lines = get_lines(verts_p)
    I = np.zeros(3)

    ykmin = np.zeros(n)
    ykmax = np.zeros(n)

    for i in range(n):
        ykmin[i] = min(verts_p[i, 1], verts_p[(i+1)%n, 1])
        ykmax[i] = max(verts_p[i, 1], verts_p[(i+1)%n, 1])

    ymin = int(min(ykmin))
    ymax = int(max(ykmax))
    return phong(
        X, verts_p, verts_n, verts_c, cam_pos, lines, ykmin, ykmax, ymin, ymax, b_coords,
        ka, kd, ks, n, light_positions, light_intensities, Ia, N, M
    )


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