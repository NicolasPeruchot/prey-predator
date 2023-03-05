from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.UserParam import Slider

from prey_predator.agents import GrassPatch, Sheep, Wolf
from prey_predator.model import WolfSheep


def wolf_sheep_portrayal(agent):
    if agent is None:
        return

    portrayal = {"Shape": "circle", "Filled": "true", "r": 0.5}

    if type(agent) is Sheep:
        portrayal["Color"] = "grey"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.8
        portrayal["text"] = str(agent.energy)
        portrayal["text_color"] = "black"

    elif type(agent) is Wolf:
        portrayal["Color"] = "red"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.8
        portrayal["text"] = str(agent.energy)
        portrayal["text_color"] = "black"

    elif type(agent) is GrassPatch:
        portrayal["Shape"] = "rect"
        portrayal["w"], portrayal["h"] = 1, 1
        portrayal["Layer"] = 1
        if agent.fully_grown:
            portrayal["Color"] = "green"
        else:
            portrayal["Color"] = "white"

    return portrayal


height = 20
width = 20

canvas_element = CanvasGrid(wolf_sheep_portrayal, width, height, 500, 500)
chart_element = ChartModule(
    [
        {"Label": "Wolves", "Color": "#AA0000"},
        {"Label": "Sheep", "Color": "#666666"},
        {"Label": "Grass", "Color": "#00FF00"},
    ]
)

model_params = {
    "height": height,
    "width": width,
    "initial_sheep": Slider("Initial sheeps", 100, 0, 200, 5),
    "initial_wolves": Slider("Initial wolves", 100, 0, 200, 5),
    "initial_grown_grass": 0.5,
    "initial_energy": Slider("Initial energy", 10, 5, 20, 1),
    "sheep_reproduce": Slider("Sheeps reproduction rate", 0.04, 0.01, 0.2, 0.01),
    "wolf_reproduce": Slider("Wolves reproduction rate", 0.05, 0.01, 0.1, 0.01),
    "wolf_gain_from_food": Slider("Gain from food (wolf)", 10, 2, 30, 1),
    "sheep_gain_from_food": Slider("Gain from food (sheep)", 10, 2, 30, 1),
    "grass": True,
    "grass_regrowth_time": Slider("Grass regrowth cooldown", 5, 2, 20, 1),
    "moore": True,
    "n_steps": 200,
}

server = ModularServer(
    WolfSheep, [canvas_element, chart_element], "Prey Predator Model", model_params
)
server.port = 8521
