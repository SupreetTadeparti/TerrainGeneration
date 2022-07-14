from pyglet.gl import *


class Model:
    def __init__(self, vao, vbos, indices):
        self.vao = vao
        self.vbos = vbos
        self.ibo = vbos[-1]
        self.indices = indices

    def set_shader(self, shader):
        self.shader = shader

    def clean_up(self):
        glDeleteVertexArrays(1, self.vao)
        for vbo in self.vbos:
            glDeleteBuffers(1, vbo)

    def bind(self, shader=None):
        if not self.shader:
            print("Shader has not been set")
            return
        self.shader.enable()
        glBindVertexArray(self.vao)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ibo)
        glEnableVertexAttribArray(0)
        glEnableVertexAttribArray(1)
        glEnableVertexAttribArray(2)

    def unbind(self):
        glDisableVertexAttribArray(2)
        glDisableVertexAttribArray(1)
        glDisableVertexAttribArray(0)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)
        glBindVertexArray(0)
