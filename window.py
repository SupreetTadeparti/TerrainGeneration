from time import time, perf_counter
from playsound import playsound
import ctypes
import math
import glm
import os
import random
from gui import GUI, Button
from renderer import Renderer
from text import Text
from entity import Entity
from objloader import OBJLoader
from world import World
from collections import defaultdict
from camera import Camera
from water import Water
from terrain import Terrain
from shader import Shader
from sun import Sun
from transformation import Transformation
from pyglet.gl import *
from pyglet.window import key
import pyglet


'''
The Window Class is the Root of the Game!

W - Forward
A - Leftward
S - Backward
D - Rightward
SPACE - Upward
LSHIFT - Downward

Press 'P' to toggle the wireframe

Hotkey between 1, 2, and 3 to change the current model

Click anywhere on the terrain or on models to place the current model there
'''


class Window(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.set_icon(pyglet.resource.image("img/icon.png"))

        self.fov=75
        self.mouse_sensitivity=0.0075
        self.frames=0
        self.wireframe=False

        self.text_shader=Shader("TextVertex", "TextFragment")
        self.gui_shader=Shader("GUIVertex", "GUIFragment")
        self.sun_shader = Shader("SunVertex", "SunFragment")
        self.bloom_sun_shader = Shader("BloomSunVertex", "BloomSunFragment")
        self.model_shader=Shader("ModelVertex",
                                   "ModelGeometry",
                                   "ModelFragment")
        self.terrain_shader=Shader("TerrainVertex",
                                     "TerrainGeometry",
                                     "TerrainFragment")
        self.water_shader=Shader("WaterVertex",
                                   "WaterGeometry",
                                   "WaterFragment")

        self.keys=defaultdict(lambda: False)

        self.projection_matrix=glm.perspective(
            glm.radians(self.fov), self.width / self.height, 0.1, 750)

        self.ortho_projection_matrix=glm.ortho(0, self.width, self.height, 0)

        self.text_shader.enable()
        self.text_shader.set_uniform_mat4(
            "u_Projection", self.ortho_projection_matrix)

        self.gui_shader.enable()
        self.gui_shader.set_uniform_mat4(
            "u_Projection", self.ortho_projection_matrix
        )

        self.bloom_sun_shader.enable()
        self.bloom_sun_shader.set_uniform_mat4(
            "u_Projection", glm.perspective(
            glm.radians(self.fov), self.width / self.height, 0.1, 1000)
        )

        self.sun_shader.enable()
        self.sun_shader.set_uniform_mat4(
            "u_Projection", glm.perspective(
            glm.radians(self.fov), self.width / self.height, 0.1, 1000)
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

        self.camera=Camera()
        self.camera.add_shader(self.terrain_shader)
        self.camera.add_shader(self.water_shader)
        self.camera.add_shader(self.model_shader)
        self.camera.add_shader(self.bloom_sun_shader)
        self.camera.add_shader(self.sun_shader)

        self.camera.move(glm.vec3(0, -150, 0))

        self.init_gui()

        self.fps_text=Text("FPS:", 10, 10)
        self.fps_count_text=Text("0", 75, 10)

        self.last=time()

        self.mouse_locked=True
        self.main_menu=True
        self.picked=False

        glReadPixels(0, 0, 1, 1, GL_DEPTH_COMPONENT,
                     GL_FLOAT, ctypes.byref(GLfloat()))

        pyglet.clock.schedule(self.update)

    def init_gui(self):
        main_menu_width=600
        main_menu_height=400
        main_menu_x=(self.width - main_menu_width) // 2
        main_menu_y=(self.height - main_menu_height) // 2
        self.title_screen=GUI(main_menu_x, main_menu_y, main_menu_width,
                                main_menu_height, (0.3, 0.3, 0.3, 1.0), self.gui_shader)

        title_button1_width=550
        title_button1_height=100
        title_button1_x=main_menu_x + (main_menu_width - title_button1_width) // 2 - 15
        title_button1_y=main_menu_y + 10
        self.title_screen.add_button(Button(
            title_button1_x, title_button1_y, title_button1_width, title_button1_height, (0, 0, 0, 0), "TERRAIN", lambda x: x, 125, False))

        title_button2_width=550
        title_button2_height=100
        title_button2_x=main_menu_x + (main_menu_width - title_button2_width) // 2 - 30
        title_button2_y=main_menu_y + 75
        self.title_screen.add_button(Button(
            title_button2_x, title_button2_y, title_button2_width, title_button2_height, (0, 0, 0, 0), "GENERATION", lambda x: x, 125, False))

        def play_button_callback(*args):
            playsound("sound\click.wav", block=False)
            self.curr_menu=self.menu
        play_button_width=250
        play_button_height=75
        play_button_x=main_menu_x + (main_menu_width - play_button_width) // 2
        play_button_y=main_menu_y + 250
        self.title_screen.add_button(Button(play_button_x, play_button_y, play_button_width,
                                            play_button_height, (0.2, 0.8, 0.2, 1.0), "PLAY", play_button_callback))

        self.curr_menu=self.title_screen

        menu_width=400
        menu_height=400
        menu_x=(self.width - menu_width) // 2
        menu_y=(self.height - menu_height) // 2
        self.menu=GUI(menu_x, menu_y, menu_width, menu_height,
                        (0.3, 0.3, 0.3, 1.0), self.gui_shader)

        def button_callback(terrain_type):
            playsound("sound\click.wav", block=False)
            return self.init_world(terrain_type)

        button_width=200
        button_height=75
        button_x=menu_x + (menu_width - button_width) // 2
        button_y=menu_y + 25
        self.menu.add_button(
            Button(button_x, button_y + (button_height + 10) * 0, button_width, button_height, (0, 0, 0, 0), "TYPE: ", lambda x: x, 60, False))
        self.menu.add_button(
            Button(button_x, button_y + (button_height + 10) * 1, button_width, button_height, (0.2, 0.8, 0.2, 1.0), "Flat", button_callback, 60))
        self.menu.add_button(
            Button(button_x, button_y + (button_height + 10) * 2, button_width, button_height, (0.2, 0.2, 0.8, 1.0), "Hills", button_callback, 60))
        self.menu.add_button(
            Button(button_x, button_y + (button_height + 10) * 3, button_width, button_height, (0.7, 0.4, 0.3, 1.0), "Mountains", button_callback, 60))

        inventory_width=225
        inventory_height=75
        inventory_x=(self.width - inventory_width) // 2
        inventory_y=self.height - inventory_height - 10
        self.inventory=GUI(inventory_x, inventory_y, inventory_width,
                             inventory_height, (0, 0, 0, 0), self.gui_shader)

        self.inventory.add_button(Button(inventory_x + (inventory_height + 5) * 0, inventory_y, inventory_height,
                                  inventory_height, (0, 50, 0, 0.5), "Tree", lambda x: x, 50, False))
        self.inventory.add_button(Button(inventory_x + (inventory_height + 5) * 1, inventory_y, inventory_height,
                                  inventory_height, (0, 0, 0, 0.75), "Bush", lambda x: x, 50, False))
        self.inventory.add_button(Button(inventory_x + (inventory_height + 5) * 2, inventory_y, inventory_height,
                                  inventory_height, (0, 0, 0, 0.75), "Rock", lambda x: x, 50, False))

        crosshair_width=25
        crosshair_height=2

        crosshair_horizontal_x=(self.width - crosshair_width) // 2
        crosshair_horizontal_y=(self.height - crosshair_height) // 2
        self.crosshair_horizontal=GUI(crosshair_horizontal_x, crosshair_horizontal_y,
                                        crosshair_width, crosshair_height, (1, 1, 1, 1), self.gui_shader)

        crosshair_vertical_x=(self.width - crosshair_height) // 2
        crosshair_vertical_y=(self.height - crosshair_width) // 2
        self.crosshair_vertical=GUI(crosshair_vertical_x, crosshair_vertical_y,
                                      crosshair_height, crosshair_width, (1, 1, 1, 1), self.gui_shader)

        self.models = {}

    def init_world(self, terrain_type):
        self.title_screen.clean_up()
        self.menu.clean_up()

        Sun.init()
        Terrain.init()
        Water.init()

        noise_magnitude=1

        if terrain_type == "Hills":
            noise_magnitude=25
        elif terrain_type == "Mountains":
            noise_magnitude=75

        self.terrain_shader.enable()
        self.terrain_shader.set_uniform_1f("u_Noise", noise_magnitude)

        self.water_shader.enable()
        self.water_shader.set_uniform_1f("u_Noise", noise_magnitude)

        self.model_shader.enable()
        self.model_shader.set_uniform_1f("u_Noise", noise_magnitude)

        self.sun = Sun(self.sun_shader, self.bloom_sun_shader, self.camera)

        self.world=World(self.camera, self.sun, self.terrain_shader,
                           self.water_shader, self.model_shader)

        self.renderer=Renderer()

        self.tree_model=OBJLoader.load_model("tree", self.model_shader)
        self.bush_model=OBJLoader.load_model("bush", self.model_shader)
        self.rock_model=OBJLoader.load_model("rock", self.model_shader)


        self.models={
            self.tree_model: Transformation(glm.vec3(), glm.vec3(-math.pi / 2, 0, 0), glm.vec3(0.05, 0.05, 0.05)),
            self.bush_model: Transformation(glm.vec3(), glm.vec3(0, 0, 0), glm.vec3(1.75, 1.75, 1.75)),
            self.rock_model: Transformation(
                glm.vec3(), glm.vec3(), glm.vec3(1.5, 1.5, 1.5))
        }

        self.model=self.tree_model

        self.main_menu=False
        self.set_exclusive_mouse()

        playsound("sound\\background.wav", block=False)

    def toggle_wireframe(self):
        if self.wireframe:
            glPolygonMode(GL_FRONT, GL_FILL)
            glPolygonMode(GL_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT, GL_LINE)
            glPolygonMode(GL_BACK, GL_LINE)
        self.wireframe=not self.wireframe

    def update(self, dt):
        if self.keys["W"]:
            self.camera.move(glm.vec3(self.camera.speed * -math.sin(self.camera.rotation.y),
                             0, self.camera.speed * math.cos(self.camera.rotation.y)))
        if self.keys["A"]:
            self.camera.move(glm.vec3(self.camera.speed * math.cos(self.camera.rotation.y),
                             0, self.camera.speed * math.sin(self.camera.rotation.y)))
        if self.keys["S"]:
            self.camera.move(glm.vec3(self.camera.speed * math.sin(self.camera.rotation.y),
                             0, self.camera.speed * -math.cos(self.camera.rotation.y)))
        if self.keys["D"]:
            self.camera.move(glm.vec3(self.camera.speed * -math.cos(self.camera.rotation.y),
                             0, self.camera.speed * -math.sin(self.camera.rotation.y)))
        if self.keys[" "]:
            self.camera.move(glm.vec3(0, -self.camera.speed, 0))
        if self.keys["LSHIFT"]:
            self.camera.move(glm.vec3(0, self.camera.speed, 0))
        if not self.main_menu:
            self.sun.update()
            self.world.update()

    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE:
            self.mouse_locked=False
            self.set_exclusive_mouse(self.mouse_locked)

        if symbol == key.W:
            self.keys["W"]=True
        if symbol == key.A:
            self.keys["A"]=True
        if symbol == key.S:
            self.keys["S"]=True
        if symbol == key.D:
            self.keys["D"]=True
        if symbol == key.SPACE:
            self.keys[" "]=True
        if symbol == key.LSHIFT:
            self.keys["LSHIFT"]=True

        if symbol == key.P:
            self.toggle_wireframe()

        if modifiers == key.MOD_CTRL and symbol == key.Z:
            self.renderer.pop_entity()

        if symbol == key._1:
            self.model=self.tree_model
            self.inventory.buttons[-1].color=glm.vec4(0, 50, 0, 0.5)
            self.inventory.buttons[-2].color=glm.vec4(0, 0, 0, 0.75)
            self.inventory.buttons[-3].color=glm.vec4(0, 0, 0, 0.75)
        elif symbol == key._2:
            self.model=self.bush_model
            self.inventory.buttons[-1].color=glm.vec4(0, 0, 0, 0.75)
            self.inventory.buttons[-2].color=glm.vec4(0, 50, 0, 0.5)
            self.inventory.buttons[-3].color=glm.vec4(0, 0, 0, 0.75)
        elif symbol == key._3:
            self.model=self.rock_model
            self.inventory.buttons[-1].color=glm.vec4(0, 0, 0, 0.75)
            self.inventory.buttons[-2].color=glm.vec4(0, 0, 0, 0.75)
            self.inventory.buttons[-3].color=glm.vec4(0, 50, 0, 0.5)

    def on_key_release(self, symbol, modifiers):
        if symbol == key.W:
            self.keys["W"]=False
        if symbol == key.A:
            self.keys["A"]=False
        if symbol == key.S:
            self.keys["S"]=False
        if symbol == key.D:
            self.keys["D"]=False
        if symbol == key.SPACE:
            self.keys[" "]=False
        if symbol == key.LSHIFT:
            self.keys["LSHIFT"]=False

    def get_depth(self):
        z=ctypes.c_float()
        glReadPixels(self.width // 2, self.height // 2, 1, 1,
                     GL_DEPTH_COMPONENT, GL_FLOAT, ctypes.byref(z))
        return z.value

    def spawn_entity(self):
        depth=self.get_depth()
        if depth == 1:
            return
        z=depth * 2 - 1
        clip_space=glm.vec4(0, 0, z, 1)
        view_space=glm.inverse(self.projection_matrix) * clip_space
        view_space /= view_space.w
        world_space=glm.inverse(self.camera.get_view()) * view_space
        translation=world_space.xyz
        rotation=self.models[self.model].rotation + random.random() / 75
        scale=self.models[self.model].scale + random.random() / 75
        transformation=Transformation(translation, rotation, scale)
        self.renderer.add_entity(Entity(self.model, transformation))

    def on_mouse_press(self, x, y, button, modifiers):
        if self.main_menu:
            self.curr_menu.click(x, self.height - y)
        else:
            self.mouse_locked=True
            self.set_exclusive_mouse(self.mouse_locked)
            self.picked=True

    def on_mouse_motion(self, x, y, dx, dy):
        y=self.height - y
        hover=False
        for button in self.curr_menu.buttons:
            if x > button.x and x < button.x + button.width and y > button.y and y < button.y + button.height and button.hover:
                hover=True
                break
        if hover:
            self.set_mouse_cursor(
                self.get_system_mouse_cursor(self.CURSOR_HAND))
        else:
            self.set_mouse_cursor(
                self.get_system_mouse_cursor(self.CURSOR_DEFAULT))
        self.camera.rotate(
            glm.vec3(-dy * self.mouse_sensitivity, dx * self.mouse_sensitivity, 0))

    def on_draw(self):
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glClearColor(0.3, 0.5, 0.8, 1.0)
        self.clear()

        if self.main_menu:
            self.curr_menu.render(self.text_shader)
        else:
            self.sun.render()
            glDisable(GL_CULL_FACE)
            self.renderer.render()
            glEnable(GL_CULL_FACE)
            glCullFace(GL_FRONT)
            self.world.render_terrain()
            if self.picked:
                self.spawn_entity()
                self.picked=False
            self.world.render_water()
            self.inventory.render(self.text_shader)
            self.crosshair_horizontal.render(self.text_shader)
            self.crosshair_vertical.render(self.text_shader)
            self.fps_text.render(self.text_shader)

        if time() - self.last >= 1:
            self.fps_text.clean_up()
            self.fps_text=Text("FPS: " + str(self.frames), 10, 10)
            self.frames=0
            self.last=time()
        else:
            self.frames += 1

    def on_close(self):
        if not self.main_menu:
            self.world.clean_up()
        for model in self.models:
            model.clean_up()
        self.terrain_shader.clean_up()
        self.water_shader.clean_up()
        self.model_shader.clean_up()
        self.text_shader.clean_up()
        self.inventory.clean_up()
        self.crosshair_horizontal.clean_up()
        self.crosshair_vertical.clean_up()
        self.close()
