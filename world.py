class World:
    def __init__(self, objects=[], paused = False, drawed_pause = False, game_won = False, game_lost = False, max_distance = 500):
        self.objects = list(objects)
        self.max_distance = max_distance
        self.paused = paused
        self.drawed_pause = drawed_pause
        self.game_won = game_won
        self.game_lost = game_lost

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
