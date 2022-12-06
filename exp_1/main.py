from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule

from CoupangModel import CoupangModel


def agent_portrayal(agent):
    portrayal = {
        "Shape": "rect",
        "Filled": "true",
        "w": 1,
        "h": 1,
        "text": agent.pos,
        "text_color": "black"}

    if agent.name == "Worker":
        if agent.unique_id == 0:
            portrayal["Color"] = "red"
            # portrayal["text"] = "서용득"
            portrayal["Layer"] = 1
        if agent.unique_id == 1:
            portrayal["Color"] = "orange"
            # portrayal["text"] = "한지훈"
            portrayal["Layer"] = 1
        if agent.unique_id == 2:
            portrayal["Color"] = "green"
            # portrayal["text"] = "이윤승"
            # portrayal["text_color"] = "white"
            portrayal["Layer"] = 1
        if agent.unique_id == 3:
            portrayal["Color"] = "royalblue"
            # portrayal["text"] = "박상준"
            # portrayal["text_color"] = "white"
            portrayal["Layer"] = 1
        if agent.unique_id == 4:
            portrayal["Color"] = "purple"
            # portrayal["text"] = "최예찬"
            # portrayal["text_color"] = "white"
            portrayal["Layer"] = 1
        if agent.unique_id == 5:
            portrayal["Color"] = "black"
            # portrayal["text"] = "이지승"
            # portrayal["text_color"] = "white"
            portrayal["Layer"] = 1
    elif agent.name == "Cart":
        if (agent.unique_id == 1000) or (agent.unique_id == 2000):
            portrayal["Color"] = "rgba(255, 0, 0, 0.6)"
            portrayal["Layer"] = 1
        if (agent.unique_id == 1001) or (agent.unique_id == 2001):
            portrayal["Color"] = "rgba(255, 165, 0, 0.6)"
            portrayal["Layer"] = 1
        if (agent.unique_id == 1002) or (agent.unique_id == 2002):
            portrayal["Color"] = "rgba(0, 128, 0, 0.6)"
            portrayal["Layer"] = 1
        if (agent.unique_id == 1003) or (agent.unique_id == 2003):
            portrayal["Color"] = "rgba(65, 105, 225, 0.6)"
            portrayal["Layer"] = 1
        if (agent.unique_id == 1004) or (agent.unique_id == 2004):
            portrayal["Color"] = "rgba(128, 0, 128, 0.6)"
            portrayal["Layer"] = 1
        if (agent.unique_id == 1005) or (agent.unique_id == 2005):
            portrayal["Color"] = "rgba(0, 0, 0, 0.6)"
            portrayal["Layer"] = 1
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
    500,
    500)

chart = ChartModule([{
    'Label': 'Total Output',
    'Color': 'Black'}],
    data_collector_name='datacollector')

server = ModularServer(
    CoupangModel,
    [grid, chart],
    "Coupang Warehouse Simulation",
    {"N": 6, "width": 17, "height": 16}
)

server.description = '''쿠팡 물류센터 픽킹 작업 시뮬레이션 - Github@서용득 : https://github.com/yongchoooon/Simulation'''

server.port = 8525  # Any non-80 port to appease replit
server.launch()
