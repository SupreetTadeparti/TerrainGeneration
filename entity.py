import glm
from pyglet.gl import *
import math


class Entity:
    def __init__(self, model, translation, rotation, scale):
        self.x = translation.x
        self.y = translation.y
        self.z = translation.z
        self.model = model
        self.matrix = \
            glm.translate(glm.mat4(1.0), glm.vec3(self.x, self.y, self.z)) \
            * glm.rotate(rotation.z, glm.vec3(0, 0, 1)) \
            * glm.rotate(rotation.y, glm.vec3(0, 1, 0)) \
            * glm.rotate(rotation.x, glm.vec3(1, 0, 0)) \
            * glm.scale(glm.vec3(scale.x, scale.y, scale.z)) \


    def render(self, shader):
        if shader is not None:
            shader.set_uniform_mat4("u_Model", self.matrix)
        else:
            self.model.shader.set_uniform_mat4("u_Model", self.matrix)
        glDrawElements(GL_TRIANGLES, self.model.indices, GL_UNSIGNED_INT, 0)
