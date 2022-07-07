"""
@author: Antonios Antoniou
@email: aantonii@ece.auth.gr
@version: Python 3.7.9
******************************
@brief: Reads the hw3.npy file to get info about the object that needs to be rendered.
        Uses the functions developed for the purposes of the first two assignments and
        adds lighting to the object.
@notes: `render` function borrowed from Anestis Kaimakamidis - 9627.
******************************
2022 Aristotle University Thessaloniki - Computer Graphics
"""

from shading import *
import numpy as np


data = np.load("h3.npy", allow_pickle=True)[()]
verts = data['verts']
vertex_colors = data['vertex_colors']
face_indices = data['face_indices']
depth = data['depth']
cam_eye = data['cam_eye']
cam_up = data['cam_up']
cam_lookat = data['cam_lookat']
ka = data['ka']
kd = data['kd']
ks = data['ks']
n = data['n']
light_positions = data['light_positions']
light_intensities = data['light_intensities']
Ia = data['Ia']
M = data['M']
N = data['N']
W = data['W']
H = data['H']
bg_color = data['bg_color']

f = 70 # taken from the second assignment data

img = render_object(
    "gouraud", f, cam_eye, cam_lookat, cam_up, bg_color, M, N, H, W,
    verts, vertex_colors, face_indices, ka, kd, ks, n, light_positions, light_intensities, Ia
)
save_image(img, "gouraud_all.jpg")

img = render_object(
    "gouraud", f, cam_eye, cam_lookat, cam_up, bg_color, M, N, H, W,
    verts, vertex_colors, face_indices, ka, 0, 0, n, light_positions, light_intensities, Ia
)
save_image(img, "gouraud_ambient.jpg")

img = render_object(
    "gouraud", f, cam_eye, cam_lookat, cam_up, bg_color, M, N, H, W,
    verts, vertex_colors, face_indices, 0, kd, 0, n, light_positions, light_intensities, Ia
)
save_image(img, "gouraud_diffuse.jpg")

img = render_object(
    "gouraud", f, cam_eye, cam_lookat, cam_up, bg_color, M, N, H, W,
    verts, vertex_colors, face_indices, 0, 0, ks, n, light_positions, light_intensities, Ia
)
save_image(img, "gouraud_specular.jpg")

img = render_object(
    "phong", f, cam_eye, cam_lookat, cam_up, bg_color, M, N, H, W,
    verts, vertex_colors, face_indices, ka, kd, ks, n, light_positions, light_intensities, Ia
)
save_image(img, "phong_all.jpg")

img = render_object(
    "phong", f, cam_eye, cam_lookat, cam_up, bg_color, M, N, H, W,
    verts, vertex_colors, face_indices, ka, 0, 0, n, light_positions, light_intensities, Ia
)
save_image(img, "phong_ambient.jpg")

img = render_object(
    "phong", f, cam_eye, cam_lookat, cam_up, bg_color, M, N, H, W,
    verts, vertex_colors, face_indices, 0, kd, 0, n, light_positions, light_intensities, Ia
)
save_image(img, "phong_diffuse.jpg")

img = render_object(
    "phong", f, cam_eye, cam_lookat, cam_up, bg_color, M, N, H, W,
    verts, vertex_colors, face_indices, 0, 0, ks, n, light_positions, light_intensities, Ia
)
save_image(img, "phong_specular.jpg")