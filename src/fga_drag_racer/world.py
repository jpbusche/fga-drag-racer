class World(object):
    def __init__(self, objects=[], max_distance=500):
        self.objects = list(objects)
        self.max_distance = max_distance
        self.paused = False
        self.drawed_pause = False
        self.game_won = False
        self.game_lost = False

    def update(self, dt):
        for obj in self.objects:
            obj.update(dt)

    def draw(self):
        for obj in self.objects:
            obj.draw()

    def add(self, obj):
        self.objects.append(obj)

    def remove(self, obj):
        self.objects.remove(obj)
