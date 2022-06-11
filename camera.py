import pyrr
import math
from vector import Vec3


def triangle_wave(x):
    return 2 / math.pi * math.asin(math.sin(math.pi * x))


class Camera:
    def __init__(self, model_shader, terrain_shader, water_shader):
        self.model_shader = model_shader
        self.terrain_shader = terrain_shader
        self.water_shader = water_shader
        self.translation_matrix = pyrr.matrix44.create_identity()
        self.rotation_matrix = pyrr.matrix44.create_identity()
        self.speed = 2
        self.position = Vec3()
        self.rotation = Vec3()
        self.move(Vec3(0, 20, 0))

    def move(self, vec):
        self.position.x -= vec.x
        self.position.y -= vec.y
        self.position.z -= vec.z
        self.translation_matrix = pyrr.matrix44.create_from_translation(
            (self.position.x, self.position.y, self.position.z))
        self.update_view()

    def rotate(self, vec):
        self.rotation.x = max(
            min(self.rotation.x + vec.x, math.pi / 2), -math.pi / 2)
        self.rotation.y += vec.y
        x_rot = pyrr.Quaternion().from_x_rotation(self.rotation.x)
        y_rot = pyrr.Quaternion().from_y_rotation(self.rotation.y)
        self.rotation_matrix = (y_rot * x_rot).matrix44
        self.update_view()

    def update_view(self):
        self.terrain_shader.enable()
        self.terrain_shader.set_uniform_mat4(
            "u_View", self.translation_matrix @ self.rotation_matrix)
        self.water_shader.enable()
        self.water_shader.set_uniform_mat4(
            "u_View", self.translation_matrix @ self.rotation_matrix)
        self.model_shader.enable()
        self.model_shader.set_uniform_mat4(
            "u_View", self.translation_matrix @ self.rotation_matrix)
