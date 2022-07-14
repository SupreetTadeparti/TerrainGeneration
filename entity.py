import glm
from pyglet.gl import *
import math


class Entity:
    def __init__(self, model, transformation):
        self.x = transformation.translation.x
        self.y = transformation.translation.y
        self.z = transformation.translation.z
        self.model = model
        self.matrix = \
            glm.translate(glm.mat4(1.0), glm.vec3(self.x, self.y, self.z)) \
            * glm.rotate(transformation.rotation.z, glm.vec3(0, 0, 1)) \
            * glm.rotate(transformation.rotation.y, glm.vec3(0, 1, 0)) \
            * glm.rotate(transformation.rotation.x, glm.vec3(1, 0, 0)) \
            * glm.scale(glm.vec3(transformation.scale.x, transformation.scale.y, transformation.scale.z)) \


    def render(self):
        self.model.shader.set_uniform_mat4("u_Model", self.matrix)
        glDrawElements(GL_TRIANGLES, self.model.indices, GL_UNSIGNED_INT, 0)
