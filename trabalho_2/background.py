class Image:
    def __init__(self, actor, x, y, identificator):
        self.actor = actor
        self.x = x
        self.y = y
        self.id = identificator

    def __eq__(self, other):
        return self.id == other.id

    def update(self, dt):
        pass

    def draw(self):
        self.actor.y = self.y
        self.actor.x = self.x
        self.actor.draw()
