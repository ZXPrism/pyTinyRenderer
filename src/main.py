from Renderer import Renderer
from random import uniform
import math

width = 1024
height = 1024

renderer = Renderer(width, height)

renderer.wireframe("tinyrenderer/african_head.obj")
# renderer.triangle((200, 100), (400, 900), (800, 500), [0.7] * 3)

renderer.render()
