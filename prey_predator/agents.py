import mesa

from mesa import Agent, Model
from mesa.space import MultiGrid

from prey_predator.random_walk import RandomWalker


class Sheep(RandomWalker):
    """
    A sheep that walks around, reproduces (asexually) and gets eaten.

    The init is the same as the RandomWalker.
    """

    energy = None

    def __init__(self, unique_id, pos, model, moore,sheep_gain_from_food, energy=None):
        super().__init__(unique_id, pos, model, moore=moore)
        self.energy = energy
        self.sheep_gain_from_food=sheep_gain_from_food
        self.item_on_cell=self.model.grid.get_cell_list_contents(([self.pos]))


    def step(self):
        """
        A model step. Move, then eat grass and reproduce.
        """
        self.random_move()
        self.energy -= 1
        grass_patch = [obj for obj in self.item_on_cell if isinstance(obj, GrassPatch)]
        if len(grass_patch) > 0:
            self.energy += self.sheep_gain_from_food
            grass_patch[0].fully_grown=False        

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

    def __init__(self, unique_id, model, fully_grown, countdown):
        """
        Creates a new patch of grass

        Args:
            grown: (boolean) Whether the patch of grass is fully grown or not
            countdown: Time for the patch of grass to be fully grown again
        """
        super().__init__(unique_id, model)
        self.fully_grown = fully_grown
        self.countdown = countdown

    def step(self):
        self.countdown -= 1
        # when the countdown is over, the grass has grown and is eatable
        if self.countdown <= 0:
            self.fully_grown = True
