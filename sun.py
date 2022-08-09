import glm
import math
import ctypes
from pyglet.gl import *
from shader import Shader
from entity import Entity
from objloader import OBJLoader
from transformation import Transformation

class Sun:
    @classmethod
    def init(cls):
        positions = []
        cls.indices = []

        radius = 40
        stack_count = 20
        sector_count = 20

        length_inv = 1.0 / radius
        sector_step = 2 * math.pi / sector_count
        stack_step = math.pi / stack_count

        for i in range(stack_count + 1):
            stack_angle = math.pi / 2 - i * stack_step
            xy = radius * math.cos(stack_angle)
            z = radius * math.sin(stack_angle)
            for j in range(sector_count + 1):
                sector_angle = j * sector_step
                x = xy * math.cos(sector_angle)
                y = xy * math.sin(sector_angle)
                positions.append(x)
                positions.append(y)
                positions.append(z)

        for i in range(stack_count):
            k1 = i * (sector_count + 1)
            k2 = k1 + sector_count + 1

            for j in range(sector_count):
                if i != 0:
                    cls.indices.append(k1)
                    cls.indices.append(k2)
                    cls.indices.append(k1 + 1)

                if i != stack_count - 1:
                    cls.indices.append(k1 + 1)
                    cls.indices.append(k2)
                    cls.indices.append(k2 + 1)
                k1 += 1
                k2 += 1

        cls.vao = ctypes.c_uint32()
        glGenVertexArrays(1, cls.vao)
        glBindVertexArray(cls.vao)

        vbo = ctypes.c_uint32()
        glGenBuffers(1, vbo)
        glBindBuffer(GL_ARRAY_BUFFER, vbo)
        glBufferData(GL_ARRAY_BUFFER, len(positions) * 4, (GLfloat * len(positions))(*positions), GL_STATIC_DRAW)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, 0)
        glBindBuffer(GL_ARRAY_BUFFER, 0)

        cls.ibo = ctypes.c_uint32()
        glGenBuffers(1, cls.ibo)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, cls.ibo)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, len(cls.indices) * 4, (GLuint * len(cls.indices))(*cls.indices), GL_STATIC_DRAW)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)

        glBindVertexArray(0)

    def __init__(self, shader, bloom_shader, camera):
        self.radius = 700
        self.shader = shader
        self.bloom_shader = bloom_shader
        self.camera = camera
        self.position = glm.vec3()
        self.da = 0.00001
        self.angle = math.radians(0)

    def update(self):
        y = self.radius * math.cos(self.angle)
        z = self.radius * math.sin(self.angle)
        self.angle += self.da
        self.position = glm.vec3(0, y, z)
        self.matrix = glm.translate(glm.mat4(1.0), self.position)

    def render(self):
        view_matrix = self.camera.rotation_matrix * glm.translate(glm.mat4(1.0), glm.vec3(0, self.camera.position.y, 0))
        self.shader.enable()
        self.shader.set_uniform_mat4("u_Model", self.matrix)
        self.shader.set_uniform_mat4("u_View", view_matrix)
        glBindVertexArray(Sun.vao)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, Sun.ibo)
        glDrawElements(GL_TRIANGLES, len(Sun.indices), GL_UNSIGNED_INT, 0)
        self.bloom_shader.enable()
        self.bloom_shader.set_uniform_3f("u_Center", self.position)
        self.bloom_shader.set_uniform_mat4("u_Model", self.matrix * glm.scale(glm.vec3(1.2, 1.2, 1.2)))
        self.bloom_shader.set_uniform_mat4("u_View", view_matrix)
        glDrawElements(GL_TRIANGLES, len(Sun.indices), GL_UNSIGNED_INT, 0)