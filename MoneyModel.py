from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from mesa.batchrunner import BatchRunner

inven_coords = [(4,12), (5,12), (6,12), (7,12), (10,12), (11,12), (12,12), (13,12),
                (4,11), (5,11), (6,11), (7,11), (10,11), (11,11), (12,11), (13,11),
                (4,8), (5,8), (6,8), (7,8), (10,8), (11,8), (12,8), (13,8),
                (4,7), (5,7), (6,7), (7,7), (10,7), (11,7), (12,7), (13,7),
                (4,4), (5,4), (6,4), (7,4), (10,4), (11,4), (12,4), (13,4),
                (4,3), (5,3), (6,3), (7,3), (10,3), (11,3), (12,3), (13,3)]

parking_lots = [(3,12),(14,12),
                (3,11),(14,11),
                (3,8),(14,8),
                (3,7),(14,7),
                (3,4),(14,4),
                (3,3),(14,3)]

conveyors = [(0,15),(1,15),(2,15),(3,15),(4,15),(5,15),(6,15),(7,15),(8,15),(9,15),(10,15),(11,15),(12,15),(13,15),(14,15),(15,15),(16,15),
             (0,14),(0,13),(0,12),(0,11),(0,10),(0,9),(0,8),(0,7),(0,6),(0,5),(0,4),(0,3),(0,2),(0,1),
             (0,0),(1,0),(2,0),(3,0),(4,0),(5,0),(6,0),(7,0),(8,0),(9,0),(10,0),(11,0),(12,0),(13,0),(14,0),(15,0),(16,0)]

obstacles = inven_coords + conveyors

all = []
for x in range(17):
    for y in range(16):
        all.append((x, y))

worker_spaces = list(set(all) - set(obstacles))

def compute_gini(model):
    # Do math here!
    agent_wealths = [agent.wealth for agent in model.schedule.agents]
    x = sorted(agent_wealths)
    N = model.num_agents
    B = sum(xi * (N - i) for i, xi in enumerate(x)) / (N * sum(x))
    return (1 + (1 / N) - 2 * B)


class MoneyAgent(Agent):
    """An agent with hopes, dreams, and a mysterious past."""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.wealth = 1
        self.name = "Worker"

    def step(self):
        self.move()
        if self.wealth > 0:
            self.give_money()

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
          self.pos,
          moore=False,
          include_center=False)
        possible_steps = list(set(possible_steps) - set(obstacles))
        print(possible_steps)
        new_position = self.random.choice(possible_steps)
        # print(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def give_money(self):
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        if len(cellmates) > 1:
            # print(cellmates[0].pos)
            other = self.random.choice(cellmates)
            other.wealth += 1
            self.wealth -= 1

class Inventory(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.name = "Inventory"
        self.wealth = -99
    
class ParkingLot(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.name = "ParkingLot"
        self.wealth = -99

class Conveyor(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.name = "Conveyor"
        self.wealth = -99

class MoneyModel(Model):
    """Our model--a home for our agents :)"""
    def __init__(self, N, width, height):
        self.num_agents = N
        # A physical world to place our agents in 
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.running = True

        # Create agents
        for i in range(self.num_agents):
            no = i
            a = MoneyAgent(no, self)
            self.schedule.add(a)
            x, y = a.random.choice(worker_spaces)
            self.grid.place_agent(a, (x, y))

        # Create inventorys
        for j in range(len(inven_coords)):
            no = j + self.num_agents
            iv = Inventory(no, self)
            self.schedule.add(iv)
            x, y = inven_coords[j]
            self.grid.place_agent(iv, (x, y))

        # Create parking lots
        for k in range(len(parking_lots)):
            no = k + no + 1
            pl = ParkingLot(no, self)
            self.schedule.add(pl)
            x, y = parking_lots[k]
            self.grid.place_agent(pl, (x, y))

        # Create conveyors
        for l in range(len(conveyors)):
            no = l + no + 1
            cv = Conveyor(no, self)
            self.schedule.add(cv)
            x, y = conveyors[l]
            self.grid.place_agent(cv, (x, y))

        # Some metrics we'll measure about our model
        self.datacollector = DataCollector(
            model_reporters={"Gini": compute_gini},
            agent_reporters={"Wealth": "wealth"},
        )

    def step(self):
        """Runs a single tick of the clock in our simulation."""
        self.datacollector.collect(self)
        self.schedule.step()
