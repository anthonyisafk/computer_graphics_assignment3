import numpy as np
import cv2 as cv


def initialize_img(M, N, bg_color):
    img = np.full((M, N, 3), bg_color)
    return img


def color_vertices(img, vert_colors, verts_rast, face_indices):
    num_faces = len(face_indices)
    for f in range(num_faces):
        current_face = face_indices[f]
        for i in range(len(current_face)):
            vert = verts_rast[current_face[i]]
            img[vert[0]][vert[1]] = vert_colors[current_face[i]]
    return img


def normalize(vec):
    norm = np.linalg.norm(vec)
    return vec / norm if norm > 0 else vec


def get_keep_indices(face_indices, verts_rast, M, N):
    num_faces = len(face_indices)
    keep_faces = []

    for i in range(num_faces):
        current_face = face_indices[i]
        face_rast = verts_rast[current_face]
        positive_indices = np.all(face_rast >= 0)
        in_bounds = np.all(face_rast[0, :] <= M - 1) and np.all(face_rast[1, :] <= N - 1)
        if positive_indices and in_bounds:
            keep_faces.append(current_face)
    return np.array(keep_faces)


def calculate_useful_depths(keep_faces, depths):
    num_keep = len(keep_faces)
    triangle_depths = np.empty((num_keep))
    for i in range(num_keep):
        triangle_depths[i] = np.mean(depths[keep_faces[i]])
    sorted_triangle_depth_idx = np.argsort(triangle_depths)[::-1] # sort in descending order

    return triangle_depths, sorted_triangle_depth_idx


def find_barycenter(verts):
    """Find the barycenter OF A TRIANGLE, given its vertex coordinates."""
    return np.sum(verts, axis=0) / 3


def save_image(img, img_w, img_h, filename: str):
	for i in range(img_w):
		for j in range(img_h):
			img[i][j] = 255 * np.flip(img[i][j])
	cv.imwrite(filename, img)