import glm
import math


class Camera:
    def __init__(self, model_shader, terrain_shader, water_shader):
        self.model_shader = model_shader
        self.terrain_shader = terrain_shader
        self.water_shader = water_shader
        self.translation_matrix = glm.mat4(1.0)
        self.rotation_matrix = glm.mat4(1.0)
        self.speed = 2
        self.position = glm.vec3(0.0, 0.0, 0.0)
        self.rotation = glm.vec3(0.0, 0.0, 0.0)
        self.move(glm.vec3(0, 20, 0))

    def move(self, vec):
        self.position.x += vec.x
        self.position.y += vec.y
        self.position.z += vec.z
        self.translation_matrix = glm.translate(self.translation_matrix, glm.vec3(
            vec.x, vec.y, vec.z))
        self.update_view()

    def rotate(self, vec):
        self.rotation.x = max(
            min(self.rotation.x + vec.x, math.pi / 2), -math.pi / 2)
        self.rotation.y += vec.y
        yaw = glm.angleAxis(self.rotation.x, glm.vec3(1, 0, 0))
        pitch = glm.angleAxis(self.rotation.y, glm.vec3(0, 1, 0))
        self.rotation_matrix = glm.mat4_cast(yaw * pitch)
        self.update_view()

    def get_view(self):
        return self.rotation_matrix * self.translation_matrix

    def update_view(self):
        self.view_matrix = self.get_view()
        self.terrain_shader.enable()
        self.terrain_shader.set_uniform_mat4(
            "u_ViewRotation", self.rotation_matrix)
        self.terrain_shader.set_uniform_mat4(
            "u_ViewTranslation", self.translation_matrix)
        self.water_shader.enable()
        self.water_shader.set_uniform_mat4(
            "u_ViewRotation", self.rotation_matrix)
        self.water_shader.set_uniform_mat4(
            "u_ViewTranslation", self.translation_matrix)
        self.model_shader.enable()
        self.model_shader.set_uniform_mat4(
            "u_ViewRotation", self.rotation_matrix)
        self.model_shader.set_uniform_mat4(
            "u_ViewTranslation", self.translation_matrix)
