import ctypes
from pyglet.gl import *


class Shader:
    def __init__(self, *args):
        vertex_source = None
        geometry_source = None
        fragment_source = None
        if len(args) == 2:
            vertex_source = args[0]
            fragment_source = args[1]
        elif len(args) == 3:
            vertex_source = args[0]
            geometry_source = args[1]
            fragment_source = args[2]
        self.vertex_shader = self.process_shader(vertex_source)
        self.fragment_shader = self.process_shader(fragment_source)
        self.geometry_shader = None
        if geometry_source is not None:
            self.geometry_shader = self.process_shader(geometry_source)
        self.create()

    def process_shader(self, name):
        lines = []
        with open("shaders/" + name + ".glsl", 'r') as reader:
            for line in reader.readlines():
                # preprocessing
                if line.startswith("#include"):
                    include_file = "shaders/" + \
                        line.split(" ")[1].replace("\n", "") + ".glsl"
                    with open(include_file, 'r') as r:
                        for l in r.readlines():
                            lines.append(l)
                else:
                    lines.append(line)
        return "".join(lines).encode("utf-8")

    def compile_shader(self, type, shader):
        id = glCreateShader(type)
        glShaderSource(id, 1, ctypes.cast(ctypes.pointer(ctypes.pointer(ctypes.create_string_buffer(
            shader))), ctypes.POINTER(ctypes.POINTER(GLchar))), None)
        glCompileShader(id)

        result = ctypes.c_int32()
        glGetShaderiv(id, GL_COMPILE_STATUS, result)

        # error handling
        if result.value == GL_FALSE:
            log_size = ctypes.c_int32()
            glGetShaderiv(id, GL_INFO_LOG_LENGTH, log_size)
            error_log = ctypes.create_string_buffer(log_size.value)
            glGetShaderInfoLog(id, log_size, None, error_log)
            glDeleteShader(id)
            shader_type = "vertex"
            if type == GL_FRAGMENT_SHADER:
                shader_type = "fragment"
            elif type == GL_GEOMETRY_SHADER:
                shader_type = "geometry"

            print(f"{shader_type.upper()} SHADER Compilation Error!")
            print(error_log.value.decode('utf-8'))

        return id

    def create(self):
        self.program = glCreateProgram()

        self.vs = self.compile_shader(GL_VERTEX_SHADER, self.vertex_shader)
        if self.geometry_shader is not None:
            self.gs = self.compile_shader(
                GL_GEOMETRY_SHADER, self.geometry_shader)
        self.fs = self.compile_shader(GL_FRAGMENT_SHADER, self.fragment_shader)

        glAttachShader(self.program, self.vs)
        if self.geometry_shader is not None:
            glAttachShader(self.program, self.gs)
        glAttachShader(self.program, self.fs)

        glLinkProgram(self.program)
        glValidateProgram(self.program)

        glDeleteShader(self.vs)
        if self.geometry_shader is not None:
            glDeleteShader(self.gs)
        glDeleteShader(self.fs)

    def uniform_location(self, uniform_name):
        return glGetUniformLocation(self.program, uniform_name.encode("ascii"))

    def set_uniform_1i(self, uniform_name, data):
        glUniform1i(self.uniform_location(uniform_name), data)

    def set_uniform_1f(self, uniform_name, data):
        glUniform1f(self.uniform_location(uniform_name), data)

    def set_uniform_2f(self, uniform_name, data):
        glUniform2f(self.uniform_location(uniform_name), *data)

    def set_uniform_3f(self, uniform_name, data):
        glUniform3f(self.uniform_location(uniform_name), *data)

    def set_uniform_4f(self, uniform_name, data):
        glUniform4f(self.uniform_location(uniform_name), *data)

    def set_uniform_mat4(self, uniform_name, data):
        glUniformMatrix4fv(self.uniform_location(uniform_name),
                           1, GL_FALSE, (ctypes.c_float * 16)(*[y for x in data for y in x]))

    def clean_up(self):
        glDetachShader(self.program, self.vs)
        if self.geometry_shader is not None:
            glDetachShader(self.program, self.gs)
        glDetachShader(self.program, self.fs)
        glDeleteProgram(self.program)

    def enable(self):
        glUseProgram(self.program)
