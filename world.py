from terrain import Terrain
from water import Water
from perlin_noise import PerlinNoise
from pyglet.gl import *


class World:
    def __init__(self, camera, terrain_shader, water_shader):
        self.terrain_shader = terrain_shader
        self.water_shader = water_shader
        self.terrain_shader.enable()
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
                self.chunks.append(Water(*chunk, self.camera))
        self.chunks = list(filter(lambda chunk: (
            chunk.worldX, chunk.worldZ) in chunks_to_render, self.chunks))

    def render(self):
        cameraChunkX = -self.camera.position.x // Terrain.SIZE
        cameraChunkZ = self.camera.position.z // Terrain.SIZE
        if cameraChunkX != self.cameraChunkX or cameraChunkZ != self.cameraChunkZ:
            self.cameraChunkX = cameraChunkX
            self.cameraChunkZ = cameraChunkZ
            self.generate_chunks()
        terrain_chunks = self.chunks[::2]
        water_chunks = self.chunks[1::2]
        self.terrain_shader.enable()
        glBindVertexArray(Terrain.vao)
        for chunk in terrain_chunks:
            chunk.render(self.terrain_shader)
        self.water_shader.enable()
        glBindVertexArray(Water.vao)
        for chunk in water_chunks:
            chunk.render(self.water_shader)

    def clean_up(self):
        glDeleteVertexArrays(1, Terrain.vao)
        glDeleteBuffers(1, Terrain.vbo)
        glDeleteBuffers(1, Terrain.ibo)
        glDeleteVertexArrays(1, Water.vao)
        glDeleteBuffers(1, Water.vbo)
        glDeleteBuffers(1, Water.ibo)
