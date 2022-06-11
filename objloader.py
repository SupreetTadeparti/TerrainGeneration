import ctypes
from model import Model
from pyglet.gl import *
import pyglet


class OBJLoader:
    @classmethod
    def load_model(cls, file):
        t = []
        n = []
        positions = []
        texture_coordinates = []
        normals = []
        indices = []
        colors = []
        color = [0, 0, 0, 1]
        mtl = ""
        f = False
        with open('models/' + file + '.obj', 'r') as reader:
            while line := reader.readline():
                if line.startswith("mtllib"):
                    mtl = line.split(" ")[1].replace("\n", "")
                elif line.startswith("usemtl"):
                    texture = line.split(" ")[1]
                    with open(f"models/{mtl}") as mtl_reader:
                        while mtl_line := mtl_reader.readline():
                            mtl_line = mtl_line.split(" ")
                            if mtl_line[0] == "newmtl" and mtl_line[1] == texture:
                                while not (mtl_line := mtl_reader.readline()).startswith("Kd"):
                                    continue
                                color = list(
                                    map(float, mtl_line.split(" ")[1:])) + [1.0]
                    for _ in range(len(positions) // 3):
                        colors += color
                elif line.startswith("v "):
                    positions.append(float(line.split(" ")[1]))
                    positions.append(float(line.split(" ")[2]))
                    positions.append(float(line.split(" ")[3]))
                elif line.startswith("vt "):
                    t.append(list(map(float, line.split(" ")[1:])))
                elif line.startswith("vn "):
                    n.append(list(map(float, line.split(" ")[1:])))
                if line.startswith("f "):
                    if not f:
                        texture_coordinates = [0] * len(positions) * 2
                        normals = [0] * len(positions) * 3
                    f = True
                    vertices = line.split(" ")[1:]
                    for vertex in vertices:
                        vertex = vertex.split("/")
                        curr = int(vertex[0]) - 1
                        indices.append(curr)
                        tex_coord = t[int(vertex[1]) - 1]
                        texture_coordinates[curr * 2] = tex_coord[0]
                        texture_coordinates[curr * 2 + 1] = 1 - tex_coord[1]
                        normal = n[int(vertex[2]) - 1]
                        normals[curr * 3 + 0] = normal[0]
                        normals[curr * 3 + 1] = normal[1]
                        normals[curr * 3 + 2] = normal[2]
                else:
                    f = False

        vao = ctypes.c_uint32()
        glGenVertexArrays(1, vao)
        glBindVertexArray(vao)

        position_vbo = ctypes.c_uint32()
        glGenBuffers(1, position_vbo)
        glBindBuffer(GL_ARRAY_BUFFER, position_vbo)
        glBufferData(GL_ARRAY_BUFFER, len(positions) * 4,
                     (GLfloat * len(positions))(*positions), GL_STATIC_DRAW)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, 0)
        glBindBuffer(GL_ARRAY_BUFFER, 0)

        normal_vbo = ctypes.c_uint32()
        glGenBuffers(1, normal_vbo)
        glBindBuffer(GL_ARRAY_BUFFER, normal_vbo)
        glBufferData(GL_ARRAY_BUFFER, len(normals) * 4,
                     (GLfloat * len(normals))(*normals), GL_STATIC_DRAW)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 0, 0)
        glBindBuffer(GL_ARRAY_BUFFER, 0)

        color_vbo = ctypes.c_uint32()
        glGenBuffers(1, color_vbo)
        glBindBuffer(GL_ARRAY_BUFFER, color_vbo)
        glBufferData(GL_ARRAY_BUFFER, len(colors) * 4,
                     (GLfloat * len(colors))(*colors), GL_STATIC_DRAW)
        glVertexAttribPointer(2, 4, GL_FLOAT, GL_FALSE, 0, 0)
        glBindBuffer(GL_ARRAY_BUFFER, 0)

        indices_vbo = ctypes.c_uint32()
        glGenBuffers(1, indices_vbo)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, indices_vbo)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, len(indices) * 4,
                     (GLint * len(indices))(*indices), GL_STATIC_DRAW)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)

        glBindVertexArray(0)

        vbos = (position_vbo, normal_vbo, color_vbo, indices_vbo)

        return Model(vao, vbos, len(indices))
