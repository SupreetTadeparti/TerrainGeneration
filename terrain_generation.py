import window
import pyglet

# Entry point

class App:
    def __init__(self):
        self.window = window.Window(1280, 720, "Terrain Generation")

    def run(self):
        pyglet.app.run()
