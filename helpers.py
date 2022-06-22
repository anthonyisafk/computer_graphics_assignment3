import numpy as np


def normalize(vec):
    norm = np.linalg.norm(vec)
    return vec / norm if norm > 0 else vec