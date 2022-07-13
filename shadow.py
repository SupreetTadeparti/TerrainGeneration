import ctypes
import glm
from shader import Shader
from pyglet.gl import *


class Shadow:
    def __init__(self):
        self.depth_map_fbo = ctypes.c_uint32()
        glGenFramebuffers(1, self.depth_map_fbo)

        self.depth_map = ctypes.c_uint32()
        glGenTextures(1, self.depth_map)
        glBindTexture(GL_TEXTURE_2D, self.depth_map)

        glTexImage2D(GL_TEXTURE_2D, 0, GL_DEPTH_COMPONENT, 1280,
                     720, 0, GL_DEPTH_COMPONENT, GL_FLOAT, 0)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)

        glBindFramebuffer(GL_FRAMEBUFFER, self.depth_map_fbo)
        glFramebufferTexture2D(
            GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT, GL_TEXTURE_2D, self.depth_map, 0)
        glDrawBuffer(GL_NONE)
        glReadBuffer(GL_NONE)
        glBindFramebuffer(GL_FRAMEBUFFER, 0)

        self.projection = glm.ortho(-35, 35, -35, 35, 0.1, 75)
        self.view = glm.lookAt(glm.vec3(0, 200, 0),
                               glm.vec3(0, 0, 0), glm.vec3(0, 1, 0))

        self.shader = Shader("ShadowVertex.glsl", "ShadowFragment.glsl")
        self.shader.enable()
        self.shader.set_uniform_mat4("u_Projection", self.projection)
        self.shader.set_uniform_mat4("u_View", self.view)

    def render(self, renderer, world):
        glViewport(0, 0, 1280, 720)
        glBindFramebuffer(GL_FRAMEBUFFER, self.depth_map_fbo)
        glClear(GL_DEPTH_BUFFER_BIT)

        # render scene
        glDisable(GL_CULL_FACE)
        renderer.render(self.shader)
        # glEnable(GL_CULL_FACE)
        # glCullFace(GL_FRONT)
        world.render_terrain(self, self.shader)
        world.render_water(self, self.shader)
        glBindFramebuffer(GL_FRAMEBUFFER, 0)
