class Background:
    def __init__(self, actor, x, y):
        self.actor = actor
        self.x = x
        self.y = y

    def update(self, dt):
        pass

    def draw(self):
        self.actor.y = self.y
        self.actor.x = self.x
        self.actor.draw()
