import mesa

from mesa import Agent, Model
from mesa.space import MultiGrid

from prey_predator.random_walk import RandomWalker

import random

class Sheep(RandomWalker):
    """
    A sheep that walks around, reproduces (asexually) and gets eaten.

    The init is the same as the RandomWalker.
    """

    energy = None

    def __init__(self, unique_id, pos, model, moore,sheep_gain_from_food,sheep_reproduce, energy=None):
        super().__init__(unique_id, pos, model, moore=moore)
        self.energy = energy
        self.sheep_gain_from_food=sheep_gain_from_food
        self.sheep_reproduce=sheep_reproduce
        self.item_on_cell=self.model.grid.get_cell_list_contents(([self.pos]))


    def step(self):
        """
        A model step. Move, then eat grass and reproduce.
        """
        self.random_move()
        self.energy -= 1
        grass_patch = [obj for obj in self.item_on_cell if isinstance(obj, GrassPatch)]
        #needed if two parents for reproduction
        #sheep_on_cell=[obj for obj in self.item_on_cell if isinstance(obj, Sheep)]

        #if there is grass on the cell, the sheep eat it and gain energy
        if len(grass_patch) > 0:
            self.energy += self.sheep_gain_from_food
            grass_patch[0].fully_grown=False   

        #needed if two parents for reproduction     
        #if len(sheep_on_cell)>0:

        #a parent has a child with proba 0.04
        if random.uniform(0, 1)< self.sheep_reproduce:
            a = Sheep(i, self) 
            #comment faire pour l'id unique ???
            self.schedule.add(a)
            self.grid.place_agent(a, self.pos)



class Wolf(RandomWalker):
    """
    A wolf that walks around, reproduces (asexually) and eats sheep.
    """

    energy = None

    def __init__(self, unique_id, pos, model, moore, energy=None):
        super().__init__(unique_id, pos, model, moore=moore)
        self.energy = energy
        '''
        self.wolf_gain_from_food=wolf_gain_from_food
        self.wolf_reproduce=wolf_reproduce
        self.item_on_cell=self.model.grid.get_cell_list_contents(([self.pos]))
        '''

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
