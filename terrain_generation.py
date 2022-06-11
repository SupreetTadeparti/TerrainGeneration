import pyglet
import window


class App:
    def __init__(self):
        self.window = window.Window(
            1280, 720, "Terrain Generation", resizable=True)

    def run(self):
        pyglet.app.run()
