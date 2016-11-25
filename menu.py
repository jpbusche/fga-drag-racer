class Menu(object):
    def __init__(self, actors=None):
        self.actors = actors
        self.id = "Menu"

    def draw(self):
        """
            This function is needed for drawing every actor in the actors list
        """
        for obj in self.actors:
            obj.draw()

    def show(self, world):
        """
            This function pauses the game and show itself on game screen
        """
        if not world.drawed_pause:
            world.drawed_pause = True
            world.paused = True
            world.add(self)
            world.draw()

    def destroy(self, world):
        """
            This function runs the game and remove itself from screen.
        """
        world.drawed_pause = False
        world.paused = False

        self.remove_from_screen()
        world.remove(self)
        world.draw()

    def remove_from_screen(self):
        """
            This function is a gambiarra. This is needed for leaving no traces
            on game screen.
        """
        for obj in self.actors:
            obj.actor.pos = 3000, 0
