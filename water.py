import ctypes
from pyglet.gl import *
from time import perf_counter
from random import random
import glm

# Every chunk in the water holds the same static model - a flat plane rectangle.

# Each vertex gets pulled up and down through a sine wave based on time in the vertex shader to create a mini-wave effect.


class Water:
    SIZE = 800
    VERTEX_COUNT = SIZE // 8
    QUAD_SIZE = SIZE // VERTEX_COUNT

    @classmethod
    def init(cls):
        cls.deltas = []
        cls.vertices = []
        cls.indices = []

        for i in range(cls.VERTEX_COUNT):
            for j in range(cls.VERTEX_COUNT):
                cls.vertices.append(j * cls.QUAD_SIZE)
                cls.vertices.append(-i * cls.QUAD_SIZE)
                cls.deltas.append(random() * 10)

        for i in range(cls.VERTEX_COUNT - 1):
            for j in range(cls.VERTEX_COUNT - 1):
                topleft = i * cls.VERTEX_COUNT + j
                topright = topleft + 1
                bottomleft = (i + 1) * cls.VERTEX_COUNT + j
                bottomright = bottomleft + 1
                cls.indices.append(topleft)
                cls.indices.append(bottomleft)
                cls.indices.append(topright)
                cls.indices.append(topright)
                cls.indices.append(bottomleft)
                cls.indices.append(bottomright)

        cls.vertices.extend(cls.deltas)

        cls.vao = ctypes.c_uint32()
        glGenVertexArrays(1, cls.vao)
        glBindVertexArray(cls.vao)

        cls.vbo = ctypes.c_uint32()
        glGenBuffers(1, cls.vbo)
        glBindBuffer(GL_ARRAY_BUFFER, cls.vbo)
        glBufferData(GL_ARRAY_BUFFER, len(cls.vertices) * 4,
                     (GLfloat * len(cls.vertices))(*cls.vertices), GL_STATIC_DRAW)

        glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 0, 0)
        glVertexAttribPointer(1, 1, GL_FLOAT, GL_FALSE, 0,
                              (len(cls.vertices) - len(cls.deltas)) * 4)

        cls.ibo = ctypes.c_uint32()
        glGenBuffers(1, cls.ibo)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, cls.ibo)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, len(cls.indices) * 4,
                     (GLuint * len(cls.indices))(*cls.indices), GL_STATIC_DRAW)

        glBindVertexArray(0)

        cls.start = perf_counter()

    def __init__(self, worldX, worldZ):
        self.worldX = worldX
        self.worldZ = worldZ

        self.matrix = glm.translate(glm.mat4(1.0), glm.vec3(
            self.worldX * (Water.SIZE - Water.QUAD_SIZE), 0, -
            self.worldZ * (Water.SIZE - Water.QUAD_SIZE)
        ))

    def render(self, shader):
        shader.set_uniform_1f("u_DeltaTime", perf_counter() - Water.start)
        shader.set_uniform_mat4("u_Model", self.matrix)
        glDrawElements(GL_TRIANGLES, len(Water.indices), GL_UNSIGNED_INT, 0)
