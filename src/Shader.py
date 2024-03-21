import numpy as np

from Model import Model
from copy import copy
from random import uniform

import Utils


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
            # Q: What about Z-coordinates? Do they need to be transformed?
        )

    def vertex(self, model: Model, triangleNo: int):
        # print(self.uniformViewMatrix)
        # print(self.uniformProjectionMatrix)

        mvp = (
            self.uniformProjectionMatrix
            @ self.uniformViewMatrix
            @ self.uniformModelMatrix
        )

        v0 = copy(model.modelData[triangleNo * 9])
        v1 = copy(model.modelData[triangleNo * 9 + 3])
        v2 = copy(model.modelData[triangleNo * 9 + 6])

        self.varyingN0 = copy(model.modelData[triangleNo * 9 + 2])
        self.varyingN1 = copy(model.modelData[triangleNo * 9 + 5])
        self.varyingN2 = copy(model.modelData[triangleNo * 9 + 8])

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

    def fragment(self, u, v):
        normalInterpolated = []
        for i in range(3):
            normalInterpolated.append(
                self.varyingN0[i] * u
                + self.varyingN1[i] * v
                + self.varyingN2[i] * (1 - u - v)
            )
        normalInterpolated = Utils.norm(normalInterpolated)
        self.fragColor = [
            Utils.clamp(Utils.dot(normalInterpolated, [0.0, 0.0, 1.0]), 0.0, 1.0)
        ] * 3
