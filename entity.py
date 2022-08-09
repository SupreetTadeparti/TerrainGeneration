import glm
from pyglet.gl import *
import math


class Entity:
    def __init__(self, model, transformation):
        self.model = model
        self.matrix = glm.mat4(1.0)
        self.translation = transformation.translation
        self.rotation = transformation.rotation
        self.scale = transformation.scale
        self.update_model_matrix()

    def set_translation(self, translation):
        self.translation = translation
        self.update_model_matrix()

    def set_rotation(self, rotation):
        self.rotation = rotation
        self.update_model_matrix()

    def set_scale(self, scale):
        self.scale = scale
        self.update_model_matrix()

    def update_model_matrix(self):
        self.matrix = \
            glm.translate(glm.mat4(1.0), self.translation) \
            * glm.rotate(self.rotation.z, glm.vec3(0, 0, 1)) \
            * glm.rotate(self.rotation.y, glm.vec3(0, 1, 0)) \
            * glm.rotate(self.rotation.x, glm.vec3(1, 0, 0)) \
            * glm.scale(self.scale)

    def render(self):
        self.model.shader.set_uniform_mat4("u_Model", self.matrix)
        glDrawElements(GL_TRIANGLES, self.model.indices, GL_UNSIGNED_INT, 0)
