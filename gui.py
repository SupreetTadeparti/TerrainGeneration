from text import Text
from pyglet.gl import *
import ctypes


class GUI:
    def __init__(self, x, y, width, height, color, shader):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.shader = shader

        positions = [
            x, y, -0.2,
            x + width, y, -0.2,
            x + width, y + height, -0.2,
            x, y + height, -0.2
        ]

        indices = [
            0, 1, 2,
            2, 3, 0
        ]

        self.vao = ctypes.c_uint32()
        glGenVertexArrays(1, self.vao)
        glBindVertexArray(self.vao)

        pvbo = ctypes.c_uint32()
        glGenBuffers(1, pvbo)
        glBindBuffer(GL_ARRAY_BUFFER, pvbo)
        glBufferData(GL_ARRAY_BUFFER, len(positions) * 4,
                     (GLfloat * len(positions))(*positions), GL_STATIC_DRAW)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, 0)
        glBindBuffer(GL_ARRAY_BUFFER, 0)

        self.ibo = ctypes.c_uint32()
        glGenBuffers(1, self.ibo)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ibo)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, len(indices) * 4,
                     (GLuint * len(indices))(*indices), GL_STATIC_DRAW)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)

        glBindVertexArray(0)

        self.buttons = []

    def add_button(self, button):
        self.buttons.append(button)

    def click(self, x, y):
        for button in self.buttons:
            if x > button.x and x < button.x + button.width:
                if y > button.y and y < button.y + button.height:
                    button.click_callback(button.text.text)

    def render(self, text_shader):
        self.shader.enable()
        self.shader.set_uniform_4f("u_Color", self.color)
        glBindVertexArray(self.vao)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ibo)
        glEnableVertexAttribArray(0)
        glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, 0)
        glDisableVertexAttribArray(0)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)
        glBindVertexArray(0)
        for button in self.buttons:
            button.render(self.shader, text_shader)


class Button:
    def __init__(self, x, y, width, height, color, text, click_callback):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.click_callback = click_callback

        positions = [
            x, y, -0.1,
            x + width, y, -0.1,
            x + width, y + height, -0.1,
            x, y + height, -0.1
        ]

        indices = [
            0, 1, 2,
            2, 3, 0
        ]

        text_width = len(text) * 15
        self.text = Text(text, x + (width - text_width) //
                         2, y + (height - 30) // 2)

        self.color = color

        self.vao = ctypes.c_uint32()
        glGenVertexArrays(1, self.vao)
        glBindVertexArray(self.vao)

        pvbo = ctypes.c_uint32()
        glGenBuffers(1, pvbo)
        glBindBuffer(GL_ARRAY_BUFFER, pvbo)
        glBufferData(GL_ARRAY_BUFFER, len(positions) * 4,
                     (GLfloat * len(positions))(*positions), GL_STATIC_DRAW)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, 0)
        glBindBuffer(GL_ARRAY_BUFFER, 0)

        self.ibo = ctypes.c_uint32()
        glGenBuffers(1, self.ibo)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ibo)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, len(indices) * 4,
                     (GLuint * len(indices))(*indices), GL_STATIC_DRAW)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)

        glBindVertexArray(0)

    def render(self, gui_shader, text_shader):
        gui_shader.enable()
        gui_shader.set_uniform_4f("u_Color", self.color)
        glBindVertexArray(self.vao)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ibo)
        glEnableVertexAttribArray(0)
        glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, 0)
        glDisableVertexAttribArray(0)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)
        glBindVertexArray(0)
        self.text.render(text_shader)
