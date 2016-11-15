class Menu:
    def __init__(self, actors = []):
        self.actors = actors
        self.id = "Menu"

    def draw(self):
        for obj in self.actors:
            obj.draw()

    def show(self, world):
        if not world.drawed_pause:
            world.drawed_pause = True
            world.paused = True
            world.add(self)
            world.draw()

    def destroy(self, world):
        world.drawed_pause = False
        world.paused = False

        self.remove_from_screen()
        world.remove(self)
        world.draw()

    def remove_from_screen(self):
        #This function is a gambiarra
        for obj in self.actors:
            obj.actor.pos = 3000, 0
