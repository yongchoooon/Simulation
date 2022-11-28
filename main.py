from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule

from MoneyModel import MoneyModel

def agent_portrayal(agent):
    portrayal = {
      "Shape": "rect",
      "Filled": "true",
      "w": 1,
      "h": 1}

    if agent.name == "Worker":
      if agent.wealth > 2:
        portrayal["Color"] = "red"
        portrayal["Layer"] = 1
      elif agent.wealth > 1:
        portrayal["Color"] = "orange"
        portrayal["Layer"] = 2
      elif agent.wealth > 0:
        portrayal["Color"] = "navy"
        portrayal["Layer"] = 3
      else:
        portrayal["Color"] = "pink"
        portrayal["Layer"] = 4
    elif agent.name == "Inventory":
      portrayal["Color"] = "#b8c6e4"
      portrayal["Layer"] = 0
    elif agent.name == "ParkingLot":
      portrayal["Color"] = "#e4eedc"
      portrayal["Layer"] = 0
    elif agent.name == "Conveyor":
      portrayal["Color"] = "lightgrey"
      portrayal["Layer"] = 0
    return portrayal

grid = CanvasGrid(
  agent_portrayal,
  17,
  16,
  800,
  800)

chart = ChartModule([{
  'Label': 'Gini',
  'Color': 'Black'}],
  data_collector_name='datacollector')

server = ModularServer(
  MoneyModel,
  [grid, chart],
  "Money Model",
  {"N":6, "width":17, "height":16}
  )
server.port = 8523 # Any non-80 port to appease replit
server.launch()