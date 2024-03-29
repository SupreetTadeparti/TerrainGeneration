import ctypes
from model import Model
from pyglet.gl import *
import pyglet

# obj loader from scratch. wasn't fun.
class OBJLoader:
    models = {}

    @classmethod
    def load_model(cls, file, shader):
        model = None
        if file not in OBJLoader.models:
            t = []
            n = []
            positions = []
            texture_coordinates = []
            normals = []
            indices = []
            colors = []
            color = [0, 0, 0, 1]
            mtl = ""
            v = []
            vn = []
            vt = []
            f = []
            g = 0
            # open model file
            with open("models/" + file + ".obj", "r") as reader:
                # for each line
                while line := reader.readline():
                    # save material file name
                    if line.startswith("mtllib"):
                        mtl = line.split(" ")[1].replace("\n", "")
                    # read material file, and load color
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
                        for _ in range(len(v)):
                            colors += color
                    # positions
                    elif line.startswith("v "):
                        v.append(line)
                    # texture coordinates
                    elif line.startswith("vt "):
                        vt.append(line)
                    # normals
                    elif line.startswith("vn "):
                        vn.append(line)
                    # connection between the three above
                    elif line.startswith("f "):
                        split = line.split(" ")
                        if len(split) == 5:
                            f.append("f " + split[1] + " " +
                                    split[2] + " " + split[3])
                            f.append("f " + split[3] + " " +
                                    split[4] + " " + split[1])
                        else:
                            f.append(line)
                    elif line.startswith("g "):
                        g += 1

            # reformatting data

            for position in v:
                positions.append(float(position.split(" ")[1]))
                positions.append(float(position.split(" ")[2]))
                positions.append(float(position.split(" ")[3]))

            for texture_coord in vt:
                t.append(list(map(float, texture_coord.split(" ")[1:])))

            for normal in vn:
                n.append(list(map(float, normal.split(" ")[1:])))

            texture_coordinates = [0] * len(positions) * 2
            normals = [0] * len(positions) * 3

            # indices and more reformatting
            for i in f:
                vertices = i.split(" ")[1:]
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

            colors *= g

            # loading data (opengl)
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

            # creating model
            model = Model(vao, vbos, len(indices))

            OBJLoader.models[file] = model
        else:
            model = OBJLoader.models[file]

        model.set_shader(shader)
        return model
