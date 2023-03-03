import mesa
from mesa import Agent, Model
from prey_predator.random_walk import RandomWalker
from mesa.space import MultiGrid

class Sheep(RandomWalker):
    """
    A sheep that walks around, reproduces (asexually) and gets eaten.

    The init is the same as the RandomWalker.
    """

    energy = None

    def __init__(self, unique_id, pos, model, moore, energy=None):
        super().__init__(unique_id, pos, model, moore=moore)
        self.energy = energy

    def step(self):
        """
        A model step. Move, then eat grass and reproduce.
        """
        self.random_move()
        self.energy-= 1
        item_on_cell=get_cell_list_contents(([self.pos]))
        is_patch=self.model.grid.get_cell_list
        # is_instance : correspondance
        if self.pos == patch.pos:
            self.energy += 10
            patch.eaten = True


class Wolf(RandomWalker):
    """
    A wolf that walks around, reproduces (asexually) and eats sheep.
    """

    energy = None

    def __init__(self, unique_id, pos, model, moore, energy=None):
        super().__init__(unique_id, pos, model, moore=moore)
        self.energy = energy

    def step(self):
        self.random_move()
        self.energy -= 1


class GrassPatch(Agent):
    """
    A patch of grass that grows at a fixed rate and it is eaten by sheep
    """

    def __init__(self, unique_id, pos, model, fully_grown, countdown):
        """
        Creates a new patch of grass

        Args:
            grown: (boolean) Whether the patch of grass is fully grown or not
            countdown: Time for the patch of grass to be fully grown again
        """
        super().__init__(unique_id, model)
        self.fully_grown=fully_grown
        self.countdown=countdown
        self.pos=pos

    def step(self):
        self.countdown -=1
        # when the countdown is over, the grass has grown and is eatable
        if self.countdown<=0:
            self.fully_grown=True
