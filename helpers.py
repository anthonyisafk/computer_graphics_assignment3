import numpy as np


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