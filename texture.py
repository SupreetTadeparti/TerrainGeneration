from pyglet.gl import *
from pyglet import image
import ctypes
import matplotlib
from PIL import Image


class Texture:
    def __init__(self, path, type="path"):
        self.texture = path if type == "image" else Image.open(path).transpose(Image.FLIP_TOP_BOTTOM)
        if self.texture.mode == "RGB":
            self.texture.putalpha(255)
        self.texture_id = ctypes.c_uint32()
        glGenTextures(1, self.texture_id)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER,
                        GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER,
                        GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA8, self.texture.width,
                     self.texture.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, self.texture.tobytes())
        glBindTexture(GL_TEXTURE_2D, 0)

    def clean_up(self):
        glDeleteTextures(1, self.texture_id)