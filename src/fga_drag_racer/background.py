class Image(object):
    def __init__(self, actor, x_pos, y_pos, identificator):
        self.actor = actor
        self.x = x_pos
        self.y = y_pos
        self.id = identificator

    def __eq__(self, other):
        return self.id == other.id

    def update(self, dt):
        pass

    def draw(self):
        self.actor.y = self.y
        self.actor.x = self.x
        self.actor.draw()
