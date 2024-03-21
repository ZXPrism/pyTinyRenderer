import numpy as np

from Renderer import Renderer
from Model import Model
from Shader import PhongShader


import Utils

width = 1024
height = 1024

renderer = Renderer(width, height)
model = Model("obj/african_head.obj")

shader = PhongShader(width, height)

shader.uniformModelMatrix = np.identity(4)
shader.uniformModelMatrix = Utils.scale(shader.uniformModelMatrix, [7] * 3)
# shader.uniformModelMatrix = Utils.translate(shader.uniformModelMatrix, [0.5, 0.5, 0.0])

shader.uniformViewMatrix = Utils.lookAt(
    [0.5, -0.5, 1.0], [0.0, 0.0, 0.0], [0.0, 1.0, 0.0]
)

shader.uniformProjectionMatrix = Utils.ortho(-10, 10, -10, 10, -0.1, -10)

renderer.useShader(shader)
renderer.modelFilled(model)

renderer.update()
