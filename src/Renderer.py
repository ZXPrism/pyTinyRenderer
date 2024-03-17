import matplotlib.pyplot as plt
import numpy as np
import Utils
from random import uniform


class Renderer:

    def __init__(self, width, height):
        self.__imgWidth = width
        self.__imgHeight = height
        self.__img = np.ones((height, width, 3))

    def render(self):
        plt.imshow(self.__img)
        plt.show()

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

        for t in Utils.fRange(0.0, 1.0, 0.01):
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

    def wireframe(self, wireframeFilePath):  # only support WaveFront OBJ Format
        obj = open(wireframeFilePath)
        lines = obj.readlines()
        obj.close()

        coords = [[]]
        for line in lines:
            item = line.strip().split(" ")

            if item[0] == "v":
                pos = list(map(float, item[1:]))
                for i in range(3):
                    pos[i] *= self.__imgWidth // 2 - 1
                    pos[i] += self.__imgWidth // 2 - 1
                    if i == 1:
                        pos[i] = self.__imgWidth - pos[i]
                coords.append(pos)

            elif item[0] == "f":
                faceData = [int(data.split("/")[0]) for data in item[1:]]
                # for v in range(3):
                #     nv = (v + 1) % 3
                #     self.line(
                #         coords[faceData[v]][0],
                #         coords[faceData[v]][1],
                #         coords[faceData[nv]][0],
                #         coords[faceData[nv]][1],
                #         [0.0, 0.0, 1.0],
                #     )
                self.triangleWireframed(
                    coords[faceData[0]],
                    coords[faceData[1]],
                    coords[faceData[2]],
                    [0.0, 0.0, 1.0],
                )

    def triangleWireframed(self, v0, v1, v2, color):
        self.line(v0[0], v0[1], v1[0], v1[1], color)
        self.line(v1[0], v1[1], v2[0], v2[1], color)
        self.line(v2[0], v2[1], v0[0], v0[1], color)

    def triangleWireframed2(self, v0, v1, v2):  # recognize different borders
        vertices = [v0, v1, v2]
        vertices.sort(lambda lhs, rhs: lhs[1] < rhs[1])

    def triangle1(self, v0, v1, v2, color):  # line sweeping algorithm
        pass

    def triangle2(self, v0, v1, v2, color):  # based on bounding box
        pass

    def triangle(self, v0, v1, v2, color):
        self.triangle2(v0, v1, v2, color)
