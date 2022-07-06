import numpy as np
from render.render_9627 import interpolate_color

from helpers import *
from lighting import *


def phong(
    img, verts2d, verts_n, vcolors, cam_pos, lines, ykmin, ykmax, ymin, ymax,
    b_coords, ka, kd, ks, n, light_positions, light_intensities, Ia, M, N
):  
    n = len(verts2d)
    normal = np.zeros(3) # placeholder for the normal vector found during each iteration.
    color = np.zeros(3) # placeholder for the color found during each iteration.
    peaks = np.zeros((2,8))
    lines_used = []
    lasti = []

    for i in range(n):
        if verts2d[i, 1] == ymin:
            peaks[0, :2] = verts2d[i]
            peaks[0, 2:5] = vcolors[i]
            peaks[0, 5:] = verts_n[i]
            lines_used = [(i+n-1)%n, i]
            lasti.append(i)
    if peaks[1][0] == 0:
        peaks[1] = peaks[0]
    if len(lasti) > 1:
        for j in range(2):
            lines_used[j] = (lasti[j] + 1) % 3

    for y in range(ymin, ymax+1):
        peaks = peaks[peaks[: , 0].argsort()]
        cross_count = 0

        for x in range(M):
            for k in range(2):
                if x == peaks[k,0]:
                    cross_count += 1
            if cross_count % 2 == 1:
                x1 = peaks[0, 0]
                x2 = peaks[1, 0]
                color = interpolate_color(x1, x2, x, peaks[0, 2:5], peaks[1, 2:5])
                normal = interpolate_normal(x1, x2, x, peaks[0, 5:], peaks[1, 5:])
                I = total_lighting(
                    b_coords, normal, color, cam_pos, ka, kd, ks, n,
                    light_positions, light_intensities, Ia
                )
                img[x, y] = I

        for j in range(3):
            if y + 1 == ykmin[j]:
                if min(ykmax) != max(ykmax):
                    lines_used.append(j)
            if y == ykmax[j] and y != ymax:
                if min(ykmin) != max(ykmin):
                    lines_used.remove(j)

        #update peaks and peak colours
        for j in range(2):
            peaks[j, 0] = int(lines[lines_used[j]](y+1, x))
            peaks[j, 1] = y+1
            peaks_of_line = [lines_used[j] , (lines_used[j]+1)%len(verts2d)]
            x1 = verts2d[peaks_of_line[0], 1]
            x2 = verts2d[peaks_of_line[1], 1]
            color = interpolate_color(x1, x2, peaks[j, 1], vcolors[peaks_of_line[0]], vcolors[peaks_of_line[1]])
            peaks[j, 5:] = interpolate_normal(x1, x2, peaks[j, 1], verts_n[peaks_of_line[0]], verts_n[peaks_of_line[1]])
            peaks[j, 2:5] = total_lighting(
                b_coords, peaks[j, 5:], color, cam_pos, ka, kd, ks, n, light_positions, light_intensities, Ia
            )
    return img


def get_lines(verts2d):
    def line1(y, x):
        if verts2d[1,1] != verts2d[0,1]:
                return (y - verts2d[0,1]) / (verts2d[1,1] - verts2d[0,1]) * (verts2d[1,0]-verts2d[0,0]) + verts2d[0,0]
        else:
            return x

    def line2(y, x):
        if verts2d[2,1] != verts2d[1,1]:
            return (y - verts2d[1,1]) / (verts2d[2,1] - verts2d[1,1]) * (verts2d[2,0]-verts2d[1,0]) + verts2d[1,0]
        else:
            return x

    def line3(y, x):
        if verts2d[0,1] != verts2d[2,1]:
            return (y - verts2d[2,1]) / (verts2d[0,1] - verts2d[2,1]) * (verts2d[0,0]-verts2d[2,0]) + verts2d[2,0]
        else:
            return x

    return [line1, line2, line3]


def interpolate_normal(x1, x2, x, N1, N2):
    N = np.zeros(3)
    if x1 != x2: 
        N = N1 + (x - x1) * (N2 - N1) / (x2 - x1) 
        return normalize(N)
    return N1