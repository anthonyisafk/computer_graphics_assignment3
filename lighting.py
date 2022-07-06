from helpers import *
import numpy as np

def ambient_light(ka, Ia):
    return ka * Ia


def diffuse_light(P, N, color, kd, light_positions, light_intensities):
    n = len(light_positions)
    I = np.zeros((n, 3))

    for i in range(n):
        L = light_positions[i] - P
        L_hat = normalize(L)
        cos_a = np.dot(N, L_hat)
        cos_a = cos_a if cos_a > 0 else 0 
        I[i] = kd * cos_a * light_intensities[i]
    return np.sum(I, axis=0) * color


def specular_light(P, N, color, cam_pos, ks, n, light_positions, light_intensities):
    s = len(light_positions)
    I = np.zeros((s, 3))
    V = cam_pos - P
    V_hat = normalize(V)

    for i in range(s):
        L = light_positions[i] - P
        L_hat = normalize(L)
        cos_a = np.dot(N, L_hat)
        cos_ba = abs(np.dot(2 * N * np.dot(N, L_hat) - L_hat, V_hat))
        if cos_ba <= 0 or cos_a <= 0:
            cos_ba = 0
        I[i] = ks * ((cos_ba) ** n) * light_intensities[i]
    return np.sum(I, axis=0) * color


def total_lighting(P, N, color, cam_pos, ka, kd, ks, n, light_positions, light_intensities, Ia):
    n = len(light_positions)
    I = np.zeros(3)
    I = ambient_light(ka, Ia) * color + \
        diffuse_light(P, N, color, kd, light_positions, light_intensities) + \
        specular_light(P, N, color, cam_pos, ks, n, light_positions, light_intensities)
    return I
