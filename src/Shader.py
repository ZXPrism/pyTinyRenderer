import numpy as np

from Model import Model
from copy import copy
from random import uniform


class PhongShader:

    uniformModelMatrix = None
    uniformViewMatrix = None
    uniformProjectionMatrix = None

    def __init__(self, imgWidth: int, imgHeight):
        self.viewportMatrix = np.array(
            [
                [imgWidth // 2, 0, 0, imgWidth // 2],
                [1, -imgHeight // 2, 0, imgHeight // 2],
                [0, 0, 1, 0],
                [0, 0, 0, 1],
            ]
        )

    def vertex(self, model: Model, triangleNo: int):
        mvp = (
            self.uniformProjectionMatrix
            @ self.uniformViewMatrix
            @ self.uniformModelMatrix
        )

        v0 = copy(model.modelData[triangleNo * 9])
        v1 = copy(model.modelData[triangleNo * 9 + 3])
        v2 = copy(model.modelData[triangleNo * 9 + 6])

        v0.append(1.0)
        v1.append(1.0)
        v2.append(1.0)

        self.position = [
            mvp @ np.array(v0),
            mvp @ np.array(v1),
            mvp @ np.array(v2),
        ]

        # perspective division, clip space --> NDC
        for i in range(3):
            self.position[i] /= self.position[i][3]

        # viewport transformation, NDC --> screen
        # Here we ignore invalid coords(outside [-1, 1] x [-1, 1]) for convenience
        # Those fragments are discarded in Renderer::setPixel(...)
        for i in range(3):
            self.position[i] = self.viewportMatrix @ self.position[i]

    def fragment(self, x, y, z):
        self.fragColor = [(z / 2 + 0.5) ** 3, (z / 2 + 0.5) ** 3, (z / 2 + 0.5) ** 3]
