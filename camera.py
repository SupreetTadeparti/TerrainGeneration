import glm
import math


class Camera:
    def __init__(self):
        self.shaders = []
        self.translation_matrix = glm.mat4(1.0)
        self.rotation_matrix = glm.mat4(1.0)
        self.speed = 2
        self.position = glm.vec3(0.0, 0.0, 0.0)
        self.rotation = glm.vec3(0.0, 0.0, 0.0)
        self.move(glm.vec3(0, 20, 0))

    def add_shader(self, shader):
        self.shaders.append(shader)

    def move(self, vec):
        self.position.x += vec.x
        self.position.y += vec.y
        self.position.z += vec.z
        self.translation_matrix = glm.translate(
            self.translation_matrix, glm.vec3(vec.x, vec.y, vec.z))
        self.update_view()

    def rotate(self, vec):
        # clamping x rotation
        self.rotation.x = max(
            min(self.rotation.x + vec.x, math.pi / 2), -math.pi / 2)
        self.rotation.y += vec.y
        # quaternions for easier rotations
        yaw = glm.angleAxis(self.rotation.x, glm.vec3(1, 0, 0))
        pitch = glm.angleAxis(self.rotation.y, glm.vec3(0, 1, 0))
        self.rotation_matrix = glm.mat4_cast(yaw * pitch)
        self.update_view()

    def get_view(self):
        return self.rotation_matrix * self.translation_matrix

    def update_view(self):
        for shader in self.shaders:
            shader.enable()
            shader.set_uniform_mat4(
                "u_ViewRotation", self.rotation_matrix)
            shader.set_uniform_mat4(
                "u_ViewTranslation", self.translation_matrix)
