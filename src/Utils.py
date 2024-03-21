import numpy as np
from math import tan, sqrt


def clamp(x, a, b):
    return a if x < a else (b if x > b else x)


def dot(v1, v2):
    res = 0
    for i in range(len(v1)):
        res += v1[i] * v2[i]
    return res


def cross(v1, v2):  # both vec3
    return [
        v1[1] * v2[2] - v1[2] * v2[1],
        v1[2] * v2[0] - v1[0] * v2[2],
        v1[0] * v2[1] - v1[1] * v2[0],
    ]


def norm(v):
    length = 0
    for comp in v:
        length += comp * comp
    length = sqrt(length)
    for comp in v:
        comp /= length
    return v


def lookAt(eye, center, up):
    # I've spending nearly half an hour to figure out how to use
    # the cross function provided by NumPy, while it kept reporting
    # mysterious errors. At the end, I gave up and implemented my own cross function.

    baseZ = [center[0] - eye[0], center[1] - eye[1], center[2] - eye[2]]
    baseZ = norm(baseZ)
    baseX = norm(cross(baseZ, up))
    baseY = cross(baseX, baseZ)

    return np.array(
        [
            [baseX[0], baseY[0], -baseZ[0], -dot(baseX, eye)],
            [baseX[1], baseY[1], -baseZ[1], -dot(baseY, eye)],
            [baseX[2], baseY[2], -baseZ[2], -dot(baseZ, eye)],
            [0, 0, 0, 1],
        ]
    )


def ortho(left, right, bottom, top, zNear, zFar):
    lx = right - left
    ly = top - bottom
    lz = zNear - zFar
    return np.array(
        [
            [2 / lx, 0, 0, -(left + right) / lx],
            [0, 2 / ly, 0, -(top + bottom) / ly],
            [0, 0, 2 / lz, -(zNear + zFar) / lz],
            [0, 0, 0, 1],
        ]
    )


def perspective(fovy, aspect, zNear, zFar):
    t = tan(fovy / 2)
    return np.array(
        [
            [1 / (aspect * t), 0, 0, 0],
            [0, 1 / t, 0, 0],
            [0, 0, zFar / (zNear - zFar), 1],
            [0, 0, zFar * zNear / (zNear - zFar), 0],
        ]
    )


def scale(matrix, scaleVec):
    matrix[0][0] *= scaleVec[0]
    matrix[1][1] *= scaleVec[1]
    matrix[2][2] *= scaleVec[2]
    return matrix


def translate(matrix, translateVec):
    return np.array(
        [
            [1, 0, 0, translateVec[0]],
            [0, 1, 0, translateVec[1]],
            [0, 0, 1, translateVec[2]],
            [0, 0, 0, 1],
        ]
        @ matrix
    )
