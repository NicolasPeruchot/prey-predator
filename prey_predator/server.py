from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule

from prey_predator.agents import GrassPatch, Sheep, Wolf
from prey_predator.model import WolfSheep


# from mesa.visualization.UserParam import UserSettableParameter


def wolf_sheep_portrayal(agent):
    if agent is None:
        return

    portrayal = {"Shape": "circle", "Filled": "true", "r": 0.5}

    if type(agent) is Sheep:
        portrayal["Color"] = "grey"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.4

    elif type(agent) is Wolf:
        portrayal["Color"] = "black"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.8

    elif type(agent) is GrassPatch:
        portrayal["Shape"] = "rect"
        portrayal["w"], portrayal["h"] = 1, 1
        portrayal["Layer"] = 1
        if agent.fully_grown:
            portrayal["Color"] = "green"
        else:
            portrayal["Color"] = "white"

    return portrayal


canvas_element = CanvasGrid(wolf_sheep_portrayal, 20, 20, 500, 500)
chart_element = ChartModule(
    [
        {"Label": "Wolves", "Color": "#AA0000"},
        {"Label": "Sheep", "Color": "#666666"},
        {"Label": "Grass", "Color": "#00FF00"},
    ]
)

model_params = {}

server = ModularServer(
    WolfSheep, [canvas_element, chart_element], "Prey Predator Model", model_params
)
server.port = 8521
