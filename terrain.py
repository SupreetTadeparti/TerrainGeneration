import ctypes
from pyglet.gl import *
from water import Water
import glm

# Every chunk in the terrain holds the same static model. The heights are modified in the vertex shader

class Terrain:
    SIZE = 800
    VERTEX_COUNT = SIZE // 8
    QUAD_SIZE = SIZE // VERTEX_COUNT

    @classmethod
    def init(cls):
        cls.vertices = [x for i in range(cls.VERTEX_COUNT) for j in range(cls.VERTEX_COUNT) for x in (
            j * Terrain.QUAD_SIZE,
            -i * Terrain.QUAD_SIZE
        )]

        cls.indices = [x for i in range(cls.VERTEX_COUNT - 1) for j in range(cls.VERTEX_COUNT - 1) for x in (
            i * cls.VERTEX_COUNT + j,
            (i + 1) * cls.VERTEX_COUNT + j,
            i * cls.VERTEX_COUNT + j + 1,
            i * cls.VERTEX_COUNT + j + 1,
            (i + 1) * cls.VERTEX_COUNT + j,
            (i + 1) * cls.VERTEX_COUNT + j + 1
        )]

        cls.vao = ctypes.c_uint32()
        glGenVertexArrays(1, cls.vao)
        glBindVertexArray(cls.vao)

        cls.vbo = ctypes.c_uint32()
        glGenBuffers(1, cls.vbo)
        glBindBuffer(GL_ARRAY_BUFFER, cls.vbo)
        glBufferData(GL_ARRAY_BUFFER, len(cls.vertices)
                     * 4, (GLfloat * len(cls.vertices))(*cls.vertices), GL_STATIC_DRAW)
        glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 0, 0)

        cls.ibo = ctypes.c_uint32()
        glGenBuffers(1, cls.ibo)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, cls.ibo)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, len(cls.indices) * 4,
                     (GLuint * len(cls.indices))(*cls.indices), GL_STATIC_DRAW)

        glBindVertexArray(0)

    def __init__(self, worldX, worldZ):
        self.worldX = worldX
        self.worldZ = worldZ
        self.matrix = glm.translate(glm.identity(glm.mat4), glm.vec3(
            self.worldX * (Terrain.SIZE - Terrain.QUAD_SIZE), 0,
            -self.worldZ * (Terrain.SIZE - Terrain.QUAD_SIZE)
        ))

    def render(self, shader):
        shader.set_uniform_mat4("u_Model", self.matrix)
        glDrawElements(GL_TRIANGLES, len(Terrain.indices), GL_UNSIGNED_INT, 0)
