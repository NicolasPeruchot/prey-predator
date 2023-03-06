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
        wolf_initial_energy=10,
        sheep_initial_energy=10,
        sheep_reproduce=0.04,
        wolf_reproduce=0.05,
        wolf_gain_from_food=20,
        sheep_gain_from_food=4,
        wolf_energy_threshold=30,
        sheep_energy_threshold=30,
        grass_probability=0.7,
        grass=True,
        grass_regrowth_time=30,
        moore=True,
        n_steps=200,
    ):
        """
        Create a new Wolf-Sheep model with the given parameters.

        Args:
            initial_sheep: Number of sheep to start with
            initial_wolves: Number of wolves to start with
            initial_grown_grass: Probability of each grass patch to be grown at the beginning
            wolf_initial_energy: intial energy for wolves
            sheep_intial_energy: intial energy for sheeps
            sheep_reproduce: Probability of each sheep reproducing each step
            wolf_reproduce: Probability of each wolf reproducing each step
            wolf_gain_from_food: Energy a wolf gains from eating a sheep
            sheep_gain_from_food: Energy sheep gain from grass, if enabled.
            wolf_energy_threshold: If the energy is above, the wolf doesn't eat
            sheep_energy_threshold: If the energy is above, the wolf doesn't eat
            grass_probability: Probability for a cell to contain grass
            grass: Whether to have the sheep eat grass for energy
            grass_regrowth_time: How long it takes for a grass patch to regrow
                                 once it is eaten
            moore : If True, may move in all 8 directions. Otherwise, only up, down, left, right
            n_steps : number of steps
        """
        super().__init__()
        # Set parameters
        self.height = height
        self.width = width
        self.initial_sheep = initial_sheep
        self.initial_wolves = initial_wolves
        self.initial_grown_grass = initial_grown_grass
        self.wolf_initial_energy = wolf_initial_energy
        self.sheep_initial_energy = sheep_initial_energy
        self.sheep_reproduce = sheep_reproduce
        self.wolf_reproduce = wolf_reproduce
        self.wolf_gain_from_food = wolf_gain_from_food
        self.grass_probability = grass_probability
        self.grass = grass
        self.grass_regrowth_time = grass_regrowth_time
        self.sheep_gain_from_food = sheep_gain_from_food
        self.wolf_energy_threshold = wolf_energy_threshold
        self.sheep_energy_threshold = sheep_energy_threshold
        self.moore = moore
        self.current_id = 1
        self.n_steps = n_steps

        self.schedule = RandomActivationByBreed(self)
        self.grid = MultiGrid(self.width, self.height, torus=True)
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
                if random.uniform(0, 1) < self.grass_probability:
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
                energy=self.sheep_initial_energy,
            )
            self.schedule.add(a)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))
            self.current_id += 1

        for _ in range(self.initial_wolves):
            a = Wolf(
                unique_id=self.current_id,
                pos=None,
                model=self,
                moore=self.moore,
                energy=self.wolf_initial_energy,
            )
            self.schedule.add(a)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))
            self.current_id += 1

    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)

    def run_model(self):
        for _ in range(self.n_steps):
            self.step()
