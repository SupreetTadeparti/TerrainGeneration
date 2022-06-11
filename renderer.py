from collections import defaultdict

class Renderer:
    def __init__(self):
        self.entities = defaultdict(lambda: [])

    def add_entity(self, entity):
        self.entities[entity.model].append(entity)
    
    def render(self):
        for model in self.entities:
            model.bind()
            for entity in self.entities[model]:
                entity.render()
            model.unbind()