import pyglet
from pyglet.window import key
from pyglet.gl import *
from shader import Shader
from terrain import Terrain
from water import Water
from camera import Camera
from collections import defaultdict
from vector import Vec3
from world import World
from objloader import OBJLoader
from entity import Entity
from text import Text
from renderer import Renderer
from gui import GUI, Button
import pyrr
import random
import math
from time import time


class Window(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fov = 50
        self.mouse_sensitivity = 0.01
        self.frames = 0
        self.wireframe = False

        self.text_shader = Shader("TextVertex.glsl", "TextFragment.glsl")
        self.gui_shader = Shader("GUIVertex.glsl", "GUIFragment.glsl")
        self.model_shader = Shader("ModelVertex.glsl",
                                   "ModelGeometry.glsl",
                                   "ModelFragment.glsl")
        self.terrain_shader = Shader("TerrainVertex.glsl",
                                     "TerrainGeometry.glsl",
                                     "TerrainFragment.glsl")
        self.water_shader = Shader("WaterVertex.glsl",
                                   "WaterGeometry.glsl",
                                   "WaterFragment.glsl")

        self.keys = defaultdict(lambda: False)

        self.projection_matrix = pyrr.matrix44.create_perspective_projection(
            self.fov, self.width / self.height, 0.1, 1000)

        self.ortho_projection_matrix = pyrr.matrix44.create_orthogonal_projection(
            0, self.width, self.height, 0, 0, 10)

        self.text_shader.enable()
        self.text_shader.set_uniform_mat4(
            "u_Projection", self.ortho_projection_matrix)

        self.gui_shader.enable()
        self.gui_shader.set_uniform_mat4(
            "u_Projection", self.ortho_projection_matrix
        )

        self.model_shader.enable()
        self.model_shader.set_uniform_mat4(
            "u_Projection", self.projection_matrix)

        self.terrain_shader.enable()
        self.terrain_shader.set_uniform_mat4(
            "u_Projection", self.projection_matrix)

        self.water_shader.enable()
        self.water_shader.set_uniform_1f("u_Height", 10)
        self.water_shader.set_uniform_mat4(
            "u_Projection", self.projection_matrix)

        self.camera = Camera(
            self.model_shader, self.terrain_shader, self.water_shader)

        menu_width = 400
        menu_height = 400
        menu_x = (self.width - menu_width) // 2
        menu_y = (self.height - menu_height) // 2
        self.menu = GUI(menu_x, menu_y, menu_width, menu_height,
                        (0.3, 0.3, 0.3, 1.0), self.gui_shader)

        def button_callback(terrain_type): return self.init_world(terrain_type)
        button_width = 200
        button_height = 75
        button_x = menu_x + (menu_width - button_width) // 2
        button_y = menu_y + 50
        self.menu.add_button(
            Button(button_x, button_y, button_width, button_height, (0.2, 0.8, 0.2, 1.0), "Flat", button_callback))
        self.menu.add_button(
            Button(button_x, button_y + button_height + 10, button_width, button_height, (0.2, 0.2, 0.8, 1.0), "Hills", button_callback))
        self.menu.add_button(
            Button(button_x, button_y + (button_height + 10) * 2, button_width, button_height, (0.7, 0.4, 0.3, 1.0), "Mountains", button_callback))

        self.fps_text = Text("FPS:", 10, 10)
        self.fps_count_text = Text("0", 75, 10)

        self.last = time()

        mouse_locked = True
        self.main_menu = True

        pyglet.clock.schedule(self.update)

    def init_world(self, terrain_type):
        Terrain.init()
        Water.init()

        noise_magnitude = 1

        if terrain_type == "Hills":
            noise_magnitude = 50
        elif terrain_type == "Mountains":
            noise_magnitude = 100

        self.model_shader.enable()
        self.model_shader.set_uniform_1f("u_Noise", noise_magnitude)
        self.terrain_shader.enable()
        self.terrain_shader.set_uniform_1f("u_Noise", noise_magnitude)

        self.world = World(self.camera, self.terrain_shader,
                           self.water_shader)
        self.renderer = Renderer()
        tree_model = OBJLoader.load_model("tree1")
        tree_model.set_shader(self.model_shader)
        for i in range(10):
            for j in range(10):
                self.renderer.add_entity(Entity(tree_model, Vec3(
                    i * 100, 0, j * 100), Vec3(math.pi / 2, 0, 0), Vec3(0.05, 0.05, 0.05)))
        self.main_menu = False
        self.set_exclusive_mouse()

    def toggle_wireframe(self):
        if self.wireframe:
            glPolygonMode(GL_FRONT, GL_FILL)
            glPolygonMode(GL_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT, GL_LINE)
            glPolygonMode(GL_BACK, GL_LINE)
        self.wireframe = not self.wireframe

    def update(self, dt):
        if self.keys["W"]:
            self.camera.move(Vec3(0, 0, -math.cos(
                self.camera.rotation.y) * self.camera.speed))
            self.camera.move(Vec3(-math.sin(
                self.camera.rotation.y) * self.camera.speed, 0, 0))
        if self.keys["A"]:
            self.camera.move(Vec3(0, 0, math.sin(
                self.camera.rotation.y) * self.camera.speed))
            self.camera.move(Vec3(-math.cos(
                self.camera.rotation.y) * self.camera.speed, 0, 0))
        if self.keys["S"]:
            self.camera.move(Vec3(0, 0, math.cos(
                self.camera.rotation.y) * self.camera.speed))
            self.camera.move(Vec3(math.sin(
                self.camera.rotation.y) * self.camera.speed, 0, 0))
        if self.keys["D"]:
            self.camera.move(Vec3(0, 0, -math.sin(
                self.camera.rotation.y) * self.camera.speed))
            self.camera.move(Vec3(math.cos(
                self.camera.rotation.y) * self.camera.speed, 0, 0))
        if self.keys[" "]:
            self.camera.move(Vec3(0, self.camera.speed, 0))
        if self.keys["LSHIFT"]:
            self.camera.move(Vec3(0, -self.camera.speed, 0))

    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE:
            mouse_locked = False
            self.set_exclusive_mouse(mouse_locked)
        if symbol == key.W:
            self.keys["W"] = True
        if symbol == key.A:
            self.keys["A"] = True
        if symbol == key.S:
            self.keys["S"] = True
        if symbol == key.D:
            self.keys["D"] = True
        if symbol == key.SPACE:
            self.keys[" "] = True
        if symbol == key.LSHIFT:
            self.keys["LSHIFT"] = True
        if symbol == key.P:
            self.toggle_wireframe()

    def on_key_release(self, symbol, modifiers):
        if symbol == key.W:
            self.keys["W"] = False
        if symbol == key.A:
            self.keys["A"] = False
        if symbol == key.S:
            self.keys["S"] = False
        if symbol == key.D:
            self.keys["D"] = False
        if symbol == key.SPACE:
            self.keys[" "] = False
        if symbol == key.LSHIFT:
            self.keys["LSHIFT"] = False

    def on_mouse_press(self, x, y, button, modifiers):
        if self.main_menu:
            self.menu.click(x, self.height - y)
        else:
            mouse_locked = True
            self.set_exclusive_mouse(mouse_locked)

    def on_mouse_motion(self, x, y, dx, dy):
        y = self.height - y
        hover = False
        for button in self.menu.buttons:
            if x > button.x and x < button.x + button.width and y > button.y and y < button.y + button.height:
                hover = True
                break
        if hover:
            self.set_mouse_cursor(
                self.get_system_mouse_cursor(self.CURSOR_HAND))
        else:
            self.set_mouse_cursor(
                self.get_system_mouse_cursor(self.CURSOR_DEFAULT))
        # if not mouse_locked:
        #     return
        self.camera.rotate(Vec3(dy * self.mouse_sensitivity,
                           -dx * self.mouse_sensitivity, 0))

    def on_draw(self):
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glClearColor(0.3, 0.5, 0.8, 1.0)
        self.clear()

        if self.main_menu:
            self.menu.render(self.text_shader)
        else:
            glDisable(GL_CULL_FACE)
            self.renderer.render()
            glEnable(GL_CULL_FACE)
            glCullFace(GL_FRONT)
            self.world.render()

        self.fps_text.render(self.text_shader)

        if time() - self.last >= 1:
            self.fps_text = Text("FPS: " + str(self.frames), 10, 10)
            self.frames = 0
            self.last = time()
        else:
            self.frames += 1

    def on_close(self):
        if not self.main_menu:
            self.world.clean_up()
        self.close()
