import matplotlib.pyplot as plt
import numpy as np

from random import uniform
from Model import Model


class Renderer:

    __shader = None

    def __init__(self, width: int, height: int):
        self.__imgWidth = width
        self.__imgHeight = height
        self.__img = np.ones((height, width, 3))
        self.__zbuffer = np.full((width, height), float("-inf"))

    def useShader(self, shader):
        self.__shader = shader

    def update(self):
        plt.imshow(self.__img)
        plt.show()

    def __checkShaderValidity(self):
        if self.__shader == None:
            print("[Renderer] A shader is necessary for rendering!")

    # low-level operations
    def setPixel(self, x, y, color):
        x = int(x)
        y = int(y)

        if x >= 0 and x < self.__imgWidth and y >= 0 and y < self.__imgHeight:
            self.__img[y][x] = color

    # high-level operations
    def line1(self, x0, y0, x1, y1, color):  # based on math equations
        # P(t) = S + tV
        S = np.array([x0, y0])  # start point
        V = np.array([x1 - x0, y1 - y0])  # direction

        tRange = [t / 100 for t in range(100)]

        for t in tRange:
            P = S + t * V
            self.setPixel(P[0], P[1], color)

    def line2(self, x0, y0, x1, y1, color):  # line1 improved / DDA
        x0 = int(x0)
        y0 = int(y0)
        x1 = int(x1)
        y1 = int(y1)

        dx = x1 - x0
        dy = y1 - y0

        if dx == 0 and dy == 0:
            self.setPixel(x0, y0, color)
            return

        if abs(dx) >= abs(dy):

            if dx < 0:
                x0, x1 = x1, x0
                y0, y1 = y1, y0

            slope = dy / dx
            for x in range(x0, x1):
                self.setPixel(x, slope * (x - x0) + y0, color)
        else:

            if dy < 0:
                x0, x1 = x1, x0
                y0, y1 = y1, y0

            slope = dx / dy
            for y in range(y0, y1):
                self.setPixel(slope * (y - y0) + x0, y, color)

    def line3(self, x0, y0, x1, y1, color):  # Bresenham's line drawing algorithm
        x0 = int(x0)
        y0 = int(y0)
        x1 = int(x1)
        y1 = int(y1)

        dx = x1 - x0
        dy = y1 - y0

        if dx == 0 and dy == 0:
            self.setPixel(x0, y0, color)
            return

        if abs(dx) >= abs(dy):

            if dx < 0:
                x0, x1 = x1, x0
                y0, y1 = y1, y0
                dx = -dx
                dy = -dy

            yOffset = 1 if dy > 0 else -1

            dy = abs(dy)

            y = y0
            P = 2 * dy - dx

            for x in range(x0, x1 + 1):
                self.setPixel(x, y, color)
                if P > 0:
                    P -= dx << 1
                    y += yOffset
                P += dy << 1
        else:
            if dy < 0:
                x0, x1 = x1, x0
                y0, y1 = y1, y0
                dx = -dx
                dy = -dy

            xOffset = 1 if dx > 0 else -1

            dx = abs(dx)

            x = x0
            P = 2 * dx - dy

            for y in range(y0, y1 + 1):
                self.setPixel(x, y, color)
                if P > 0:
                    P -= dy << 1
                    x += xOffset
                P += dx << 1

    def line(self, x0, y0, x1, y1, color):
        self.line3(x0, y0, x1, y1, color)

    def modelWireframed(self, model: Model):  # only support WaveFront OBJ Format
        for i in range(model.triangleNum):
            self.__shader.vertex(model, i)

            self.triangleWireframed(
                self.__shader.position[0],
                self.__shader.position[1],
                self.__shader.position[2],
                [0.0, 0.0, 1.0],
            )

    def modelFilled(self, model: Model):  # only support WaveFront OBJ Format
        for i in range(model.triangleNum):
            self.__shader.vertex(model, i)

            self.triangle(
                self.__shader.position[0],
                self.__shader.position[1],
                self.__shader.position[2],
                [0.0, 0.0, 1.0],
            )

    def triangleWireframed(self, v0, v1, v2, color):
        self.line(v0[0], v0[1], v1[0], v1[1], color)
        self.line(v1[0], v1[1], v2[0], v2[1], color)
        self.line(v2[0], v2[1], v0[0], v0[1], color)

    def triangleWireframed2(self, v0, v1, v2):  # recognize different borders
        vertices = [v0, v1, v2]
        vertices.sort(key=lambda x: x[1])
        self.line(
            vertices[0][0],
            vertices[0][1],
            vertices[1][0],
            vertices[1][1],
            [1.0, 0.0, 0.0],
        )
        self.line(
            vertices[1][0],
            vertices[1][1],
            vertices[2][0],
            vertices[2][1],
            [0.0, 1.0, 0.0],
        )
        self.line(
            vertices[2][0],
            vertices[2][1],
            vertices[0][0],
            vertices[0][1],
            [0.0, 0.0, 1.0],
        )

    def triangle1(self, v0, v1, v2, color):  # line sweeping algorithm
        vertices = [v0, v1, v2]
        vertices.sort(key=lambda x: x[1])

        # 1. draw the contour
        self.triangleWireframed(v0, v1, v2, color)

        # 2. fill the triangle
        slopeInv2 = (vertices[0][0] - vertices[2][0]) / (
            vertices[0][1] - vertices[2][1]
        )

        for i in range(2):
            v0 = list(map(int, vertices[i]))
            v1 = list(map(int, vertices[i + 1]))
            v2 = list(map(int, vertices[(i + 2) % 3]))
            if v0[1] != v1[1]:
                slopeInv1 = (v1[0] - v0[0]) / (v1[1] - v0[1])
                for y in range(v0[1] + 1, v1[1] + 1):
                    self.line(
                        slopeInv1 * (y - v0[1]) + v0[0],
                        y,
                        slopeInv2 * (y - vertices[0][1]) + vertices[0][0],
                        y,
                        color,
                    )

        # 3. (optional) highlight the contour for test
        # self.triangleWireframed(vertices[0], vertices[1], vertices[2], [1.0, 0.0, 0.0])

    def triangle2(self, v0, v1, v2, color):  # based on barycentric coordinates

        # 1. Find the bounding box of the given triangle
        minX = int(min(v0[0], v1[0], v2[0]))
        maxX = int(max(v0[0], v1[0], v2[0]))
        minY = int(min(v0[1], v1[1], v2[1]))
        maxY = int(max(v0[1], v1[1], v2[1]))

        # 2. For every pixels inside the triangle, draw it

        def barycentric(x, y, v0, v1, v2):
            vec1 = [v2[0] - v0[0], v2[0] - v1[0], v2[0] - x]
            vec2 = [v2[1] - v0[1], v2[1] - v1[1], v2[1] - y]
            res = [  # res = cross_product(vec1, vec2)
                vec1[1] * vec2[2] - vec1[2] * vec2[1],
                vec1[2] * vec2[0] - vec1[0] * vec2[2],
                vec1[0] * vec2[1] - vec1[1] * vec2[0],
            ]
            u = res[0] / -res[2]
            v = res[1] / -res[2]

            return (
                u >= 0 and v >= 0 and u + v <= 1,
                u * (v2[2] - v0[2]) + v * (v2[2] - v1[2]),
            )

        for x in range(minX, maxX + 1):
            for y in range(minY, maxY + 1):
                (inside, z) = barycentric(x, y, v0, v1, v2)
                if inside:
                    if self.__zbuffer[x][y] > z:
                        continue
                    self.__zbuffer[x][y] = z

                    if self.__shader != None:
                        self.__shader.fragment(x, y, z)
                        self.setPixel(x, y, self.__shader.fragColor)
                    else:
                        self.setPixel(x, y, color)

        # 3. (optional) highlight the contour for test
        # self.triangleWireframed(v0, v1, v2, [1.0, 0.0, 0.0])

    def triangle(self, v0, v1, v2, color):
        self.triangle2(v0, v1, v2, color)
