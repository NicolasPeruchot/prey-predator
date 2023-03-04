"""
Prey-Predator Model
================================

Replication of the model found in NetLogo:
    Wilensky, U. (1997). NetLogo Wolf Sheep Predation model.
    http://ccl.northwestern.edu/netlogo/models/WolfSheepPredation.
    Center for Connected Learning and Computer-Based Modeling,
    Northwestern University, Evanston, IL.
"""

import random

from mesa import Model
from mesa.datacollection import DataCollector
from mesa.space import MultiGrid

from prey_predator.agents import GrassPatch, Sheep, Wolf
from prey_predator.schedule import RandomActivationByBreed


class WolfSheep(Model):
    """
    Wolf-Sheep Predation Model

    A model for simulating wolf and sheep (predator-prey) ecosystem modelling.

    """

    def __init__(
        self,
        height=20,
        width=20,
        initial_sheep=100,
        initial_wolves=50,
        initial_grown_grass=0.5,
        initial_energy=10,
        sheep_reproduce=0.04,
        wolf_reproduce=0.05,
        wolf_gain_from_food=20,
        grass=True,
        grass_regrowth_time=30,
        sheep_gain_from_food=4,
        moore=True,
    ):
        """
        Create a new Wolf-Sheep model with the given parameters.

        Args:
            initial_sheep: Number of sheep to start with
            initial_wolves: Number of wolves to start with
            initial_grown_grass: Probability of each grass patch to be grown at the beginning
            initial_energy: intial energy for sheeps and wolves
            sheep_reproduce: Probability of each sheep reproducing each step
            wolf_reproduce: Probability of each wolf reproducing each step
            wolf_gain_from_food: Energy a wolf gains from eating a sheep
            grass: Whether to have the sheep eat grass for energy
            grass_regrowth_time: How long it takes for a grass patch to regrow
                                 once it is eaten
            sheep_gain_from_food: Energy sheep gain from grass, if enabled.
            moore : If True, may move in all 8 directions. Otherwise, only up, down, left, right
        """
        super().__init__()
        # Set parameters
        self.height = height
        self.width = width
        self.initial_sheep = initial_sheep
        self.initial_wolves = initial_wolves
        self.initial_grown_grass = initial_grown_grass
        self.initial_energy = initial_energy
        self.sheep_reproduce = sheep_reproduce
        self.wolf_reproduce = wolf_reproduce
        self.wolf_gain_from_food = wolf_gain_from_food
        self.grass = grass
        self.grass_regrowth_time = grass_regrowth_time
        self.sheep_gain_from_food = sheep_gain_from_food
        self.moore = moore
        self.current_id = 1

        self.schedule = RandomActivationByBreed(self)
        self.grid = MultiGrid(self.height, self.width, torus=True)
        self.datacollector = DataCollector(
            {
                "Wolves": lambda m: m.schedule.get_breed_count(Wolf),
                "Sheep": lambda m: m.schedule.get_breed_count(Sheep),
                "Grass": lambda m: len(
                    [
                        grass
                        for grass in m.schedule.agents
                        if isinstance(grass, GrassPatch) and grass.fully_grown
                    ]
                ),
            }
        )

        for x in range(self.grid.width):
            for y in range(self.grid.height):
                a = GrassPatch(
                    unique_id=self.current_id,
                    model=self,
                    fully_grown=random.uniform(0, 1) < self.initial_grown_grass,
                    countdown=self.grass_regrowth_time,
                )
                self.schedule.add(a)
                self.grid.place_agent(a, (x, y))
                self.current_id += 1

        for _ in range(self.initial_sheep):
            a = Sheep(
                unique_id=self.current_id,
                pos=None,
                model=self,
                moore=self.moore,
                energy=self.initial_energy,
            )
            self.schedule.add(a)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))
            self.current_id += 1

        # for _ in range(self.initial_wolves):
        #     a = Wolf(self.current_id, self)
        #     self.schedule.add(a)
        #     x = self.random.randrange(self.grid.width)
        #     y = self.random.randrange(self.grid.height)
        #     self.grid.place_agent(a, (x, y))
        #     self.current_id += 1

    def step(self):
        self.schedule.step()

        # Collect data
        self.datacollector.collect(self)

        # ... to be completed

    def run_model(self, step_count=200):
        for _ in range(step_count):
            self.step()
