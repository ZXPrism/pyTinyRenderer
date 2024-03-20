import numpy as np

from Renderer import Renderer
from Model import Model
from Shader import PhongShader

width = 1024
height = 1024

renderer = Renderer(width, height)
model = Model("tinyrenderer/african_head.obj")

shader = PhongShader(width, height)
shader.uniformModelMatrix = np.identity(4)
shader.uniformViewMatrix = np.identity(4)
shader.uniformProjectionMatrix = np.identity(4)

renderer.useShader(shader)
renderer.modelFilled(model)

renderer.update()
