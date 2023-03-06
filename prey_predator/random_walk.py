"""
Generalized behavior for random walking, one grid cell at a time.
"""

import random

from mesa import Agent


class RandomWalker(Agent):
    """
    Class implementing random walker methods in a generalized manner.

    Not indended to be used on its own, but to inherit its methods to multiple
    other agents.

    """

    def __init__(self, unique_id, pos, model, energy, moore=True):
        """
        grid: The MultiGrid object in which the agent lives.
        x: The agent's current x coordinate
        y: The agent's current y coordinate
        moore: If True, may move in all 8 directions.
                Otherwise, only up, down, left, right.
        energy: current energy of the agent
        """
        super().__init__(unique_id, model)
        self.pos = pos
        self.energy = energy
        self.moore = moore

    def random_move(self):
        """
        Step one cell in any allowable direction.
        """
        # Pick the next cell from the adjacent cells.
        next_moves = self.model.grid.get_neighborhood(self.pos, self.moore, True)
        next_move = self.random.choice(next_moves)
        # Now move:
        self.model.grid.move_agent(self, next_move)

    def breed(self, proba, energy):
        """
        Breed a new agent based on a given probability.
        """
        if random.uniform(0, 1) < proba:
            a = self.__class__(
                unique_id=self.model.current_id,
                pos=None,
                model=self.model,
                moore=True,
                energy=energy,
            )
            self.model.schedule.add(a)
            self.model.grid.place_agent(a, self.pos)
            self.model.current_id += 1
