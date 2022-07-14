import matplotlib
from PIL import Image, ImageDraw, ImageFont
from texture import Texture
import ctypes
from pyglet.gl import *

# Turns out text in games is just joined images of each character. My attempt on that. Text may not be perfect

class Text:

    def __init__(self, text, x, y, font_size=60):
        self.x = x
        self.y = y
        self.font_size = font_size
        self.char_width = self.font_size // 4
        self.char_height = self.font_size // 2
        self.text = text
        self.width = len(self.text) * self.char_width
        self.height = self.char_height
        image = Image.new("RGB", (self.width, self.height))
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype("fonts/font.ttf", self.font_size)
        draw.text((0, 0), text, font=font)
        self.texture = Texture(
            self.rotate_image(image), type="image")
        self.position = [self.x, self.y, -0.01,
                         self.x + self.width, self.y, -0.01,
                         self.x + self.width, self.y + self.height, -0.01,
                         self.x, self.y + self.height, -0.01]
        self.texcoords = [0, 0, 0, 1, 1, 1, 1, 0]
        self.indices = [0, 1, 2, 2, 3, 0]

        self.vao = ctypes.c_uint32()
        glGenVertexArrays(1, self.vao)
        glBindVertexArray(self.vao)

        self.pvbo = ctypes.c_uint32()
        glGenBuffers(1, self.pvbo)
        glBindBuffer(GL_ARRAY_BUFFER, self.pvbo)
        glBufferData(GL_ARRAY_BUFFER, len(self.position) * 4,
                     (GLfloat * len(self.position))(*self.position), GL_STATIC_DRAW)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, 0)

        self.tvbo = ctypes.c_uint32()
        glGenBuffers(1, self.tvbo)
        glBindBuffer(GL_ARRAY_BUFFER, self.tvbo)
        glBufferData(GL_ARRAY_BUFFER, len(self.texcoords) * 4,
                     (GLfloat * len(self.texcoords))(*self.texcoords), GL_STATIC_DRAW)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 0, 0)

        self.ibo = ctypes.c_uint32()
        glGenBuffers(1, self.ibo)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ibo)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, len(self.indices) * 4,
                     (GLuint * len(self.indices))(*self.indices), GL_STATIC_DRAW)

        glBindVertexArray(0)

    def rotate_image(self, img):
        new_img = Image.new("RGB", (img.height, img.width))
        pix1 = new_img.load()
        pix2 = img.load()
        for i in range(img.width):
            for j in range(img.height):
                pix1[j, i] = pix2[i, j]
        return new_img

    def clean_up(self):
        glDeleteVertexArrays(1, self.vao)
        glDeleteBuffers(1, self.pvbo)
        glDeleteBuffers(1, self.tvbo)
        glDeleteBuffers(1, self.ibo)
        self.texture.clean_up()

    def render(self, shader):
        shader.enable()
        glBindVertexArray(self.vao)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texture.texture_id)
        shader.set_uniform_1i("u_Texture", 0)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ibo)
        glEnableVertexAttribArray(0)
        glEnableVertexAttribArray(1)
        glDrawElements(GL_TRIANGLES, len(self.indices), GL_UNSIGNED_INT, 0)
        glDisableVertexAttribArray(1)
        glDisableVertexAttribArray(0)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)
        glBindTexture(GL_TEXTURE_2D, 0)
        glBindVertexArray(0)
