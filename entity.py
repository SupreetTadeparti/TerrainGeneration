import pyrr
from pyglet.gl import *
import math


class Entity:
    def __init__(self, model, translation, rotation, scale):
        self.x = translation.x
        self.y = translation.y
        self.z = translation.z
        self.model = model
        self.matrix = pyrr.matrix44.create_from_scale((scale.x, scale.y, scale.z)) @ \
            pyrr.matrix44.create_from_x_rotation(rotation.x) @ \
            pyrr.matrix44.create_from_y_rotation(rotation.y) @ \
            pyrr.matrix44.create_from_z_rotation(rotation.z) @ \
            pyrr.matrix44.create_from_translation((self.x, self.y, self.z))

    def render(self):
        self.model.shader.set_uniform_2f("u_Position", (self.x, self.z))
        self.model.shader.set_uniform_mat4("u_Model", self.matrix)
        glDrawElements(GL_TRIANGLES, self.model.indices, GL_UNSIGNED_INT, 0)
