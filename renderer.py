from collections import defaultdict


class Renderer:
    def __init__(self):
        self.entities = defaultdict(lambda: [])
        self.stack = []

    def add_entity(self, entity):
        self.entities[entity.model].append(entity)
        self.stack.append(entity.model)

    def pop_entity(self):
        self.entities[self.stack[-1]].pop(-1)
        self.stack.pop(-1)

    def render(self, shader=None):
        for model in self.entities:
            if shader is not None:
                model.bind(shader)
            else:
                model.bind()
            for entity in self.entities[model]:
                entity.render(shader)
            model.unbind()
