from mesa import Agent

from prey_predator.random_walk import RandomWalker


def remove_agent(agent):
    agent.model.grid.remove_agent(agent)
    agent.model.schedule.remove(agent)


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
            current_countdown : Current value of the cooldown
        """
        super().__init__(unique_id, model)
        self.fully_grown = fully_grown
        self.countdown = countdown
        self.current_countdown = countdown

    def step(self):
        if self.fully_grown is not True:
            self.current_countdown -= 1
            # when the countdown is over, the grass has grown and is eatable
            if self.current_countdown <= 0:
                self.fully_grown = True


class Sheep(RandomWalker):
    """
    A sheep that walks around, reproduces (asexually) and gets eaten.

    The init is the same as the RandomWalker.
    """

    def __init__(self, unique_id, pos, model, energy, moore):
        super().__init__(unique_id, pos, model, energy, moore)
        self.energy = energy

    def step(self):
        """
        A model step. Move, then eat grass and reproduce.
        """
        self.random_move()
        self.energy -= 1

        # If a sheep has no more energy, it dies
        if self.energy == 0:
            remove_agent(self)

        else:
            item_on_cell = self.model.grid.get_cell_list_contents(([self.pos]))

            if self.model.grass:
                grass_patch = [
                    obj
                    for obj in item_on_cell
                    if isinstance(obj, GrassPatch) and obj.fully_grown is True
                ]

                # if there is grass on the cell, the sheep eat it and gain energy.
                # The grass cooldown is then reinitilized
                if grass_patch:
                    self.energy += self.model.sheep_gain_from_food
                    grass_patch[0].fully_grown = False
                    grass_patch[0].current_countdown = grass_patch[0].countdown

            # A parent has a child with a given probability
            self.breed(self.model.sheep_reproduce)


class Wolf(RandomWalker):
    """
    A wolf that walks around, reproduces (asexually) and eats sheep.
    """

    energy = None

    def __init__(self, unique_id, pos, model, moore, energy):
        super().__init__(unique_id, pos, model, moore)
        self.energy = energy

    def step(self):
        self.random_move()
        self.energy -= 1

        # If a wolf has no more energy, it dies
        if self.energy == 0:
            remove_agent(self)

        else:
            item_on_cell = self.model.grid.get_cell_list_contents(([self.pos]))
            sheeps = [obj for obj in item_on_cell if isinstance(obj, Sheep) is True]

            # if there is a sheep on the cell, the wolf eat it and gain energy.
            # The sheep then dies
            # A wolf eats only one sheep per step
            if sheeps:
                self.energy += self.model.wolf_gain_from_food
                remove_agent(sheeps[0])

            # A parent has a child with a given probability
            self.breed(self.model.sheep_reproduce)
