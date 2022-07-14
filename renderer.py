from collections import defaultdict

'''
Model Renderer :-
Model -> List of Entities
'''


class Renderer:
    def __init__(self):
        self.entities = defaultdict(lambda: [])

        # stack for ctrl+z purposes
        self.stack = []

    def add_entity(self, entity):
        self.entities[entity.model].append(entity)
        self.stack.append(entity.model)

    def pop_entity(self):
        self.entities[self.stack[-1]].pop(-1)
        self.stack.pop(-1)

    def render(self):
        for model in self.entities:
            model.bind()
            for entity in self.entities[model]:
                entity.render()
            model.unbind()
