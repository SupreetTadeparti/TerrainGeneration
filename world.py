from terrain import Terrain
from water import Water
from perlin_noise import PerlinNoise
from pyglet.gl import *
from random import randint


class World:
    def __init__(self, camera, terrain_shader, water_shader, model_shader):
        self.terrain_shader = terrain_shader
        self.water_shader = water_shader
        self.model_shader = model_shader
        self.terrain_shader.enable()
        offset_x = randint(-250, 250)
        offset_z = randint(-250, 250)
        self.terrain_shader.set_uniform_1f("u_OffsetX", offset_x)
        self.terrain_shader.set_uniform_1f("u_OffsetZ", offset_z)
        self.water_shader.enable()
        self.water_shader.set_uniform_1f("u_OffsetX", offset_x)
        self.water_shader.set_uniform_1f("u_OffsetZ", offset_z)
        self.model_shader.enable()
        self.model_shader.set_uniform_1f("u_OffsetX", offset_x)
        self.model_shader.set_uniform_1f("u_OffsetZ", offset_z)
        self.camera = camera
        self.cameraChunkX = 0
        self.cameraChunkZ = 0
        self.chunks = []
        self.generate_chunks()

    def generate_chunks(self):
        chunks_to_render = [
            (self.cameraChunkX - 1, self.cameraChunkZ - 1),
            (self.cameraChunkX, self.cameraChunkZ - 1),
            (self.cameraChunkX + 1, self.cameraChunkZ - 1),
            (self.cameraChunkX - 1, self.cameraChunkZ),
            (self.cameraChunkX, self.cameraChunkZ),
            (self.cameraChunkX + 1, self.cameraChunkZ),
            (self.cameraChunkX - 1, self.cameraChunkZ + 1),
            (self.cameraChunkX, self.cameraChunkZ + 1),
            (self.cameraChunkX + 1, self.cameraChunkZ + 1),
        ]
        for chunk in chunks_to_render:
            if not any(c.worldX == chunk[0] and c.worldZ == chunk[1] for c in self.chunks):
                self.chunks.append(Terrain(*chunk))
                self.chunks.append(Water(*chunk))
        self.chunks = list(filter(lambda chunk: (
            chunk.worldX, chunk.worldZ) in chunks_to_render, self.chunks))

    def update(self):
        cameraChunkX = -self.camera.position.x // Terrain.SIZE
        cameraChunkZ = self.camera.position.z // Terrain.SIZE
        if cameraChunkX != self.cameraChunkX or cameraChunkZ != self.cameraChunkZ:
            self.cameraChunkX = cameraChunkX
            self.cameraChunkZ = cameraChunkZ
            self.generate_chunks()

    def render_terrain(self, shadow, shader=None):
        terrain_chunks = self.chunks[::2]
        if shader is None:
            self.terrain_shader.enable()
            self.terrain_shader.set_uniform_1i("u_ShadowMap", 0)
            self.terrain_shader.set_uniform_mat4(
                "u_LightProjection", shadow.projection)
            self.terrain_shader.set_uniform_mat4("u_LightView", shadow.view)
            glBindTexture(GL_TEXTURE_2D, shadow.depth_map)
            glActiveTexture(GL_TEXTURE0)
        else:
            shader.enable()
        glBindVertexArray(Terrain.vao)
        for chunk in terrain_chunks:
            chunk.render(self.terrain_shader if shader is None else shader)

    def render_water(self, shadow, shader=None):
        water_chunks = self.chunks[1::2]
        if shader is None:
            self.water_shader.enable()
        else:
            shader.enable()
        glBindVertexArray(Water.vao)
        for chunk in water_chunks:
            chunk.render(self.water_shader if shader is None else shader)

    def clean_up(self):
        glDeleteVertexArrays(1, Terrain.vao)
        glDeleteBuffers(1, Terrain.vbo)
        glDeleteBuffers(1, Terrain.ibo)
        glDeleteVertexArrays(1, Water.vao)
        glDeleteBuffers(1, Water.vbo)
        glDeleteBuffers(1, Water.ibo)
