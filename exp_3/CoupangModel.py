from mesa import Agent, Model
from mesa.time import BaseScheduler
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from mesa.model import Model

import random
from collections import deque
from scipy.spatial import distance as dst

inven_coords = [(4, 12), (5, 12), (6, 12), (7, 12), (10, 12), (11, 12), (12, 12), (13, 12),
                (4, 11), (5, 11), (6, 11), (7, 11), (10,
                                                     11), (11, 11), (12, 11), (13, 11),
                (4, 8), (5, 8), (6, 8), (7, 8), (10, 8), (11, 8), (12, 8), (13, 8),
                (4, 7), (5, 7), (6, 7), (7, 7), (10, 7), (11, 7), (12, 7), (13, 7),
                (4, 4), (5, 4), (6, 4), (7, 4), (10, 4), (11, 4), (12, 4), (13, 4),
                (4, 3), (5, 3), (6, 3), (7, 3), (10, 3), (11, 3), (12, 3), (13, 3),
                (3, 12), (14, 12),
                (3, 11), (14, 11),
                (3, 8), (14, 8),
                (3, 7), (14, 7),
                (3, 4), (14, 4),
                (3, 3), (14, 3)]

conveyors = [(0, 15), (1, 15), (2, 15), (3, 15), (4, 15), (5, 15), (6, 15), (7, 15), (8, 15), (9, 15), (10, 15), (11, 15), (12, 15), (13, 15), (14, 15), (15, 15), (16, 15),
             (0, 14), (0, 13), (0, 12), (0, 11), (0, 10), (0, 9), (0,
                                                                   8), (0, 7), (0, 6), (0, 5), (0, 4), (0, 3), (0, 2), (0, 1),
             (0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0), (9, 0), (10, 0), (11, 0), (12, 0), (13, 0), (14, 0), (15, 0), (16, 0)]

obstacles = inven_coords + conveyors

workplaces = [(3, 13), (4, 13), (5, 13), (6, 13), (7, 13), (10, 13), (11, 13), (12, 13), (13, 13), (14, 13),
              (3, 10), (4, 10), (5, 10), (6, 10), (7, 10), (10,
                                                            10), (11, 10), (12, 10), (13, 10), (14, 10),
              (3, 9), (4, 9), (5, 9), (6, 9), (7, 9), (10,
                                                       9), (11, 9), (12, 9), (13, 9), (14, 9),
              (3, 6), (4, 6), (5, 6), (6, 6), (7, 6), (10,
                                                       6), (11, 6), (12, 6), (13, 6), (14, 6),
              (3, 5), (4, 5), (5, 5), (6, 5), (7, 5), (10,
                                                       5), (11, 5), (12, 5), (13, 5), (14, 5),
              (3, 2), (4, 2), (5, 2), (6, 2), (7, 2), (10,
                                                       2), (11, 2), (12, 2), (13, 2), (14, 2)
              ]


front_of_conveyors = [(1, 14), (2, 14), (3, 14), (4, 14), (5, 14), (6, 14), (7, 14), (8, 14), (9, 14), (10, 14), (11, 14), (12, 14), (13, 14), (14, 14), (15, 14), (16, 14),
                      (1, 13), (1, 12), (1, 11), (1, 10), (1, 9), (1, 8), (1,
                                                                           7), (1, 6), (1, 5), (1, 4), (1, 3), (1, 2), (1, 1),
                      (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1), (8, 1), (9, 1), (10, 1), (11, 1), (12, 1), (13, 1), (14, 1), (15, 1), (16, 1)]

start_agent_spaces = [(1, 14), (1, 8), (1, 1), (16, 14), (16, 8), (16, 1)]
start_cart1_spaces = [(1, 13), (1, 7), (1, 2), (16, 13), (16, 7), (16, 2)]
start_cart2_spaces = [(1, 12), (1, 6), (1, 3), (16, 12), (16, 6), (16, 3)]

agent_pos_cart3 = [0, 0, 0, 0, 0, 0]
agent_pos_cart2 = [0, 0, 0, 0, 0, 0]
agent_pos_cart1 = [0, 0, 0, 0, 0, 0]
agent_pos_nows = [0, 0, 0, 0, 0, 0]

previous_pos_deque = [deque([(), (), (), (), ()]) for _ in range(6)]

steps = 1


###################################################
# 기록원

# 1. 각 작업자의 생산량 및 총 생산량
output = [0, 0, 0, 0, 0, 0]

# 2. 각 작업자의 평균 작업시간 (= 총 작업 step / 한 사이클 작업 완료 횟수)
working_steps = [0, 0, 0, 0, 0, 0]
working_counts = [0, 0, 0, 0, 0, 0]

###################################################
# 실험지
# 1. Inventory 60
# inven_coords = inven_coords
# workplaces = workplaces
# obstacles = inven_coords + conveyors

# # 2. Inventory 56
# inven_coords = [(3, 12), (4, 12), (5, 12), (6, 12), (7, 12), (10, 12), (11, 12), (12, 12), (13, 12), (14, 12),
#                 (3, 11), (4, 11), (5, 11), (6, 11), (7, 11), (10,
#                                                               11), (11, 11), (12, 11), (13, 11), (14, 11),
#                 (3, 8), (4, 8), (5, 8), (6, 8), (11, 8), (12, 8), (13, 8), (14, 8),
#                 (3, 7), (4, 7), (5, 7), (6, 7), (11, 7), (12, 7), (13, 7), (14, 7),
#                 (3, 4), (4, 4), (5, 4), (6, 4), (7, 4), (10,
#                                                          4), (11, 4), (12, 4), (13, 4), (14, 4),
#                 (3, 3), (4, 3), (5, 3), (6, 3), (7, 3), (10, 3), (11, 3), (12, 3), (13, 3), (14, 3)]
# workplaces = [(3, 13), (4, 13), (5, 13), (6, 13), (7, 13), (10, 13), (11, 13), (12, 13), (13, 13), (14, 13),
#               (3, 10), (4, 10), (5, 10), (6, 10), (7, 10), (10,
#                                                             10), (11, 10), (12, 10), (13, 10), (14, 10),
#               (3, 9), (4, 9), (5, 9), (6, 9), (11, 9), (12, 9), (13, 9), (14, 9),
#               (3, 6), (4, 6), (5, 6), (6, 6), (11, 6), (12, 6), (13, 6), (14, 6),
#               (3, 5), (4, 5), (5, 5), (6, 5), (7, 5), (10,
#                                                        5), (11, 5), (12, 5), (13, 5), (14, 5),
#               (3, 2), (4, 2), (5, 2), (6, 2), (7, 2), (10, 2), (11, 2), (12, 2), (13, 2), (14, 2)]
# obstacles = inven_coords + conveyors

# # 3. Inventory 52
inven_coords = [(4, 12), (5, 12), (6, 12), (7, 12), (10, 12), (11, 12), (12, 12), (13, 12),
                (4, 11), (5, 11), (6, 11), (7, 11), (10,
                                                     11), (11, 11), (12, 11), (13, 11),
                (3, 8), (4, 8), (5, 8), (6, 8), (11, 8), (12, 8), (13, 8), (14, 8),
                (3, 7), (4, 7), (5, 7), (6, 7), (11, 7), (12, 7), (13, 7), (14, 7),
                (3, 4), (4, 4), (5, 4), (6, 4), (7, 4), (10,
                                                         4), (11, 4), (12, 4), (13, 4), (14, 4),
                (3, 3), (4, 3), (5, 3), (6, 3), (7, 3), (10, 3), (11, 3), (12, 3), (13, 3), (14, 3)]
workplaces = [(4, 13), (5, 13), (6, 13), (7, 13), (10, 13), (11, 13), (12, 13), (13, 13),
              (4, 10), (5, 10), (6, 10), (7, 10), (10,
                                                   10), (11, 10), (12, 10), (13, 10),
              (3, 9), (4, 9), (5, 9), (6, 9), (11, 9), (12, 9), (13, 9), (14, 9),
              (3, 6), (4, 6), (5, 6), (6, 6), (11, 6), (12, 6), (13, 6), (14, 6),
              (3, 5), (4, 5), (5, 5), (6, 5), (7, 5), (10,
                                                       5), (11, 5), (12, 5), (13, 5), (14, 5),
              (3, 2), (4, 2), (5, 2), (6, 2), (7, 2), (10, 2), (11, 2), (12, 2), (13, 2), (14, 2)]
obstacles = inven_coords + conveyors

# # 4. Inventory 48
# inven_coords = [(4, 12), (5, 12), (6, 12), (7, 12), (10, 12), (11, 12), (12, 12), (13, 12),
#                 (4, 11), (5, 11), (6, 11), (7, 11), (10,
#                                                      11), (11, 11), (12, 11), (13, 11),
#                 (3, 8), (4, 8), (5, 8), (6, 8), (11, 8), (12, 8), (13, 8), (14, 8),
#                 (3, 7), (4, 7), (5, 7), (6, 7), (11, 7), (12, 7), (13, 7), (14, 7),
#                 (4, 4), (5, 4), (6, 4), (7, 4), (10,
#                                                  4), (11, 4), (12, 4), (13, 4),
#                 (4, 3), (5, 3), (6, 3), (7, 3), (10, 3), (11, 3), (12, 3), (13, 3)]
# workplaces = [(4, 13), (5, 13), (6, 13), (7, 13), (10, 13), (11, 13), (12, 13), (13, 13),
#               (4, 10), (5, 10), (6, 10), (7, 10), (10,
#                                                    10), (11, 10), (12, 10), (13, 10),
#               (3, 9), (4, 9), (5, 9), (6, 9), (11, 9), (12, 9), (13, 9), (14, 9),
#               (3, 6), (4, 6), (5, 6), (6, 6), (11, 6), (12, 6), (13, 6), (14, 6),
#               (4, 5), (5, 5), (6, 5), (7, 5), (10, 5), (11, 5), (12, 5), (13, 5),
#               (4, 2), (5, 2), (6, 2), (7, 2), (10, 2), (11, 2), (12, 2), (13, 2)]
# obstacles = inven_coords + conveyors

# # 5. Inventory 44
# inven_coords = [(4, 12), (5, 12), (6, 12), (7, 12), (10, 12), (11, 12), (12, 12), (13, 12),
#                 (4, 11), (5, 11), (6, 11), (7, 11), (10,
#                                                      11), (11, 11), (12, 11), (13, 11),
#                 (3, 8), (4, 8), (5, 8), (12, 8), (13, 8), (14, 8),
#                 (3, 7), (4, 7), (5, 7), (12, 7), (13, 7), (14, 7),
#                 (4, 4), (5, 4), (6, 4), (7, 4), (10,
#                                                  4), (11, 4), (12, 4), (13, 4),
#                 (4, 3), (5, 3), (6, 3), (7, 3), (10, 3), (11, 3), (12, 3), (13, 3)]
# workplaces = [(4, 13), (5, 13), (6, 13), (7, 13), (10, 13), (11, 13), (12, 13), (13, 13),
#               (4, 10), (5, 10), (6, 10), (7, 10), (10,
#                                                    10), (11, 10), (12, 10), (13, 10),
#               (3, 9), (4, 9), (5, 9), (12, 9), (13, 9), (14, 9),
#               (3, 6), (4, 6), (5, 6), (12, 6), (13, 6), (14, 6),
#               (4, 5), (5, 5), (6, 5), (7, 5), (10, 5), (11, 5), (12, 5), (13, 5),
#               (4, 2), (5, 2), (6, 2), (7, 2), (10, 2), (11, 2), (12, 2), (13, 2)]
# obstacles = inven_coords + conveyors

# # 6. Inventory 40
# inven_coords = [(5, 12), (6, 12), (7, 12), (10, 12), (11, 12), (12, 12),
#                 (5, 11), (6, 11), (7, 11), (10, 11), (11, 11), (12, 11),
#                 (3, 8), (4, 8), (5, 8), (12, 8), (13, 8), (14, 8),
#                 (3, 7), (4, 7), (5, 7), (12, 7), (13, 7), (14, 7),
#                 (4, 4), (5, 4), (6, 4), (7, 4), (10,
#                                                  4), (11, 4), (12, 4), (13, 4),
#                 (4, 3), (5, 3), (6, 3), (7, 3), (10, 3), (11, 3), (12, 3), (13, 3)]
# workplaces = [(5, 13), (6, 13), (7, 13), (10, 13), (11, 13), (12, 13),
#               (5, 10), (6, 10), (7, 10), (10, 10), (11, 10), (12, 10),
#               (3, 9), (4, 9), (5, 9), (12, 9), (13, 9), (14, 9),
#               (3, 6), (4, 6), (5, 6), (12, 6), (13, 6), (14, 6),
#               (4, 5), (5, 5), (6, 5), (7, 5), (10, 5), (11, 5), (12, 5), (13, 5),
#               (4, 2), (5, 2), (6, 2), (7, 2), (10, 2), (11, 2), (12, 2), (13, 2)]
# obstacles = inven_coords + conveyors


# # 7. Inventory 36
# inven_coords = [(5, 12), (6, 12), (7, 12), (10, 12), (11, 12), (12, 12),
#                 (5, 11), (6, 11), (7, 11), (10, 11), (11, 11), (12, 11),
#                 (3, 8), (4, 8), (5, 8), (12, 8), (13, 8), (14, 8),
#                 (3, 7), (4, 7), (5, 7), (12, 7), (13, 7), (14, 7),
#                 (5, 4), (6, 4), (7, 4), (10, 4), (11, 4), (12, 4),
#                 (5, 3), (6, 3), (7, 3), (10, 3), (11, 3), (12, 3),]
# workplaces = [(5, 13), (6, 13), (7, 13), (10, 13), (11, 13), (12, 13),
#               (5, 10), (6, 10), (7, 10), (10, 10), (11, 10), (12, 10),
#               (3, 9), (4, 9), (5, 9), (12, 9), (13, 9), (14, 9),
#               (3, 6), (4, 6), (5, 6), (12, 6), (13, 6), (14, 6),
#               (5, 5), (6, 5), (7, 5), (10, 5), (11, 5), (12, 5),
#               (5, 2), (6, 2), (7, 2), (10, 2), (11, 2), (12, 2)]
# obstacles = inven_coords + conveyors

# # 8. Inventory 32
# inven_coords = [(5, 12), (6, 12), (7, 12), (10, 12), (11, 12), (12, 12),
#                 (5, 11), (6, 11), (7, 11), (10, 11), (11, 11), (12, 11),
#                 (3, 8), (4, 8), (13, 8), (14, 8),
#                 (3, 7), (4, 7), (13, 7), (14, 7),
#                 (5, 4), (6, 4), (7, 4), (10, 4), (11, 4), (12, 4),
#                 (5, 3), (6, 3), (7, 3), (10, 3), (11, 3), (12, 3)]
# workplaces = [(5, 13), (6, 13), (7, 13), (10, 13), (11, 13), (12, 13),
#               (5, 10), (6, 10), (7, 10), (10, 10), (11, 10), (12, 10),
#               (3, 9), (4, 9), (13, 9), (14, 9),
#               (3, 6), (4, 6), (13, 6), (14, 6),
#               (5, 5), (6, 5), (7, 5), (10, 5), (11, 5), (12, 5),
#               (5, 2), (6, 2), (7, 2), (10, 2), (11, 2), (12, 2)]
# obstacles = inven_coords + conveyors

# # 9. Inventory 28
# inven_coords = [(6, 12), (7, 12), (10, 12), (11, 12),
#                 (6, 11), (7, 11), (10, 11), (11, 11),
#                 (3, 8), (4, 8), (13, 8), (14, 8),
#                 (3, 7), (4, 7), (13, 7), (14, 7),
#                 (5, 4), (6, 4), (7, 4), (10, 4), (11, 4), (12, 4),
#                 (5, 3), (6, 3), (7, 3), (10, 3), (11, 3), (12, 3)]
# workplaces = [(6, 13), (7, 13), (10, 13), (11, 13),
#               (6, 10), (7, 10), (10, 10), (11, 10),
#               (3, 9), (4, 9), (13, 9), (14, 9),
#               (3, 6), (4, 6), (13, 6), (14, 6),
#               (5, 5), (6, 5), (7, 5), (10, 5), (11, 5), (12, 5),
#               (5, 2), (6, 2), (7, 2), (10, 2), (11, 2), (12, 2)]
# obstacles = inven_coords + conveyors

# # 10. Inventory 24
# inven_coords = [(6, 12), (7, 12), (10, 12), (11, 12),
#                 (6, 11), (7, 11), (10, 11), (11, 11),
#                 (3, 8), (4, 8), (13, 8), (14, 8),
#                 (3, 7), (4, 7), (13, 7), (14, 7),
#                 (6, 4), (7, 4), (10, 4), (11, 4),
#                 (6, 3), (7, 3), (10, 3), (11, 3)]
# workplaces = [(6, 13), (7, 13), (10, 13), (11, 13),
#               (6, 10), (7, 10), (10, 10), (11, 10),
#               (3, 9), (4, 9), (13, 9), (14, 9),
#               (3, 6), (4, 6), (13, 6), (14, 6),
#               (6, 5), (7, 5), (10, 5), (11, 5),
#               (6, 2), (7, 2), (10, 2), (11, 2)]
# obstacles = inven_coords + conveyors


# # 11. Inventory 20
# inven_coords = [(6, 12), (7, 12), (10, 12), (11, 12),
#                 (6, 11), (7, 11), (10, 11), (11, 11),
#                 (3, 8), (14, 8),
#                 (3, 7), (14, 7),
#                 (6, 4), (7, 4), (10, 4), (11, 4),
#                 (6, 3), (7, 3), (10, 3), (11, 3)]
# workplaces = [(6, 13), (7, 13), (10, 13), (11, 13),
#               (6, 10), (7, 10), (10, 10), (11, 10),
#               (3, 9), (14, 9),
#               (3, 6), (14, 6),
#               (6, 5), (7, 5), (10, 5), (11, 5),
#               (6, 2), (7, 2), (10, 2), (11, 2)]
# obstacles = inven_coords + conveyors

# # 12. Inventory 16
# inven_coords = [(7, 12), (10, 12),
#                 (7, 11), (10, 11),
#                 (3, 8), (14, 8),
#                 (3, 7), (14, 7),
#                 (6, 4), (7, 4), (10, 4), (11, 4),
#                 (6, 3), (7, 3), (10, 3), (11, 3)]
# workplaces = [(7, 13), (10, 13),
#               (7, 10), (10, 10),
#               (3, 9), (14, 9),
#               (3, 6), (14, 6),
#               (6, 5), (7, 5), (10, 5), (11, 5),
#               (6, 2), (7, 2), (10, 2), (11, 2)]
# obstacles = inven_coords + conveyors

# # 13. Inventory 12
# inven_coords = [(7, 12), (10, 12),
#                 (7, 11), (10, 11),
#                 (3, 8), (14, 8),
#                 (3, 7), (14, 7),
#                 (7, 4), (10, 4),
#                 (7, 3), (10, 3)]
# workplaces = [(7, 13), (10, 13),
#               (7, 10), (10, 10),
#               (3, 9), (14, 9),
#               (3, 6), (14, 6),
#               (7, 5), (10, 5),
#               (7, 2), (10, 2)]
# obstacles = inven_coords + conveyors

# # 14. Inventory 8
# inven_coords = [(3, 12), (14, 12),
#                 (3, 11), (14, 11),
#                 (3, 4),  (14, 4),
#                 (3, 3), (14, 3)]
# workplaces = [(3, 13), (14, 13),
#               (3, 10), (14, 10),
#               (3, 5), (14, 5),
#               (3, 2), (14, 2)
#               ]
# obstacles = inven_coords + conveyors

###################################################

revival = 100
workplaces_copy = workplaces.copy()
workplaces_arrive_counts = [5 for _ in range(len(workplaces))]
workplaces_revival_counts = [revival for _ in range(len(workplaces))]


def total_output(model):  # 에이전트당 평균 생산량
    total_output = sum(output)
    return total_output


class Worker(Agent):
    """An agent with hopes, dreams, and a mysterious past."""

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.name = "Worker"
        self.num_remaining_work = 5
        self.allocate_workplace()
        self.previous_pos = start_agent_spaces[self.unique_id]
        agent_pos_cart1[self.unique_id] = start_cart1_spaces[self.unique_id]

    def step(self):
        if self.num_remaining_work == -1:  # 컨베이어로 가면 -1이 되는데 그렇게 되면 5개로 할당해라
            self.allocate_work()
            self.allocate_workplace()

        if self.is_done_with_work():  # 일이 끝났으면 컨베이어 위치를 타겟으로 지정해라
            self.set_target_to_conveyor()
            if self.is_arrived_at_target_place():
                self.num_remaining_work -= 1
                output[self.unique_id] += 5  # 기록 1
                working_counts[self.unique_id] += 1  # 기록 2
        elif self.is_arrived_at_target_place():  # 일이 아직 안 끝난 상태이고 목표위치와 내 위치가 같으면 새로 위치를 할당해라
            print(self.unique_id, ': ', self.pos)
            if workplaces_arrive_counts[workplaces_copy.index(self.pos)] == 0:
                workplaces.remove(self.pos)
                workplaces_arrive_counts[workplaces_copy.index(self.pos)] = 5
                workplaces_revival_counts[workplaces_copy.index(self.pos)] -= 1
            else:
                workplaces_arrive_counts[workplaces_copy.index(self.pos)] -= 1

            working_steps[self.unique_id] += 1  # 기록 2
            self.num_remaining_work -= 1
            if self.is_done_with_work():
                self.set_target_to_conveyor()
            else:
                self.allocate_workplace()
        else:
            working_steps[self.unique_id] += 1  # 기록 2

        agent_pos_cart1[self.unique_id] = self.pos
        self.move()
        agent_pos_nows[self.unique_id] = self.pos

        print(len(workplaces))
        # print("remaining works : ", self.num_remaining_work)
        # print("target : ", self.target_place)
        # print("now : ", self.pos)
        # print("-------------------------------------------------------")

    def allocate_work(self):
        self.num_remaining_work = 5

    def allocate_workplace(self):
        workplace = random.choice(workplaces)
        self.target_place = workplace

    def is_arrived_at_target_place(self):
        return self.pos == self.target_place

    def is_done_with_work(self):
        return self.num_remaining_work == 0

    def set_target_to_conveyor(self):
        front_of_conveyors_place = self.optimum_step(
            front_of_conveyors, self.pos)
        self.target_place = front_of_conveyors_place

    def optimum_step(self, possible_steps, target):
        possible_steps_dsts = []
        if len(possible_steps) != 0:
            for step in possible_steps:
                possible_steps_dsts.append(dst.euclidean(target, step))

                optimum_step = possible_steps[min(
                    range(len(possible_steps_dsts)), key=lambda i:possible_steps_dsts[i])]

        else:
            optimum_step = self.pos
        return optimum_step

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=False,
            include_center=False)

        now = agent_pos_nows + agent_pos_cart1 + agent_pos_cart3

        possible_steps = list(set(possible_steps) -
                              set(obstacles) - set([self.previous_pos]) - set(now))
        new_position = self.optimum_step(possible_steps, self.target_place)
        self.previous_pos = self.pos
        previous_pos_deque[self.unique_id].append(self.previous_pos)
        previous_pos_deque[self.unique_id].popleft()
        if previous_pos_deque[self.unique_id][0] == previous_pos_deque[self.unique_id][-1]:
            rand = random.random()
            if rand <= 0.3:
                new_position = self.pos
        self.model.grid.move_agent(self, new_position)


class Inventory(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.name = "Inventory"


class Conveyor(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.name = "Conveyor"


class Workplace(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.name = "Workplace"

    def step(self):
        if workplaces_revival_counts[workplaces_copy.index(self.pos)] != revival:
            workplaces_revival_counts[workplaces_copy.index(self.pos)] -= 1
            if (workplaces_arrive_counts[workplaces_copy.index(self.pos)] == 5) and (workplaces_revival_counts[workplaces_copy.index(self.pos)] == 0):
                workplaces.append(self.pos)
                workplaces_revival_counts[workplaces_copy.index(
                    self.pos)] = revival


class Cart1(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.name = "Cart"

    def step(self):
        self.parent_id = self.unique_id - 1000
        agent_pos_cart2[self.parent_id] = self.pos
        self.model.grid.move_agent(self, agent_pos_cart1[self.parent_id])
        agent_pos_cart3[self.parent_id] = self.pos


class Cart2(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.name = "Cart"

    def step(self):
        self.parent_id = self.unique_id - 2000
        self.model.grid.move_agent(self, agent_pos_cart2[self.parent_id])


class CoupangModel(Model):
    def __init__(self, N, width, height):
        self.num_agents = N
        # A physical world to place our agents in
        self.grid = MultiGrid(width, height, True)
        self.schedule = BaseScheduler(self)
        self.running = True

        # Create agents
        for i in range(self.num_agents):
            no = i
            a = Worker(no, self)
            self.schedule.add(a)
            x, y = start_agent_spaces[i]
            self.grid.place_agent(a, (x, y))

        # Create workplaces
        for k in range(len(workplaces)):
            no = no + k + 5000
            w = Workplace(no, self)
            self.schedule.add(w)
            x, y = workplaces[k]
            self.grid.place_agent(w, (x, y))

        # Create cart1s
        for c in range(self.num_agents):
            no = c + 1000
            c1 = Cart1(no, self)
            self.schedule.add(c1)
            x, y = start_cart1_spaces[c]
            self.grid.place_agent(c1, (x, y))

        # Create cart2s
        for d in range(self.num_agents):
            no = d + 2000
            c2 = Cart2(no, self)
            self.schedule.add(c2)
            x, y = start_cart2_spaces[d]
            self.grid.place_agent(c2, (x, y))

        # Create inventorys
        for j in range(len(inven_coords)):
            no = no + j + self.num_agents
            iv = Inventory(no, self)
            self.schedule.add(iv)
            x, y = inven_coords[j]
            self.grid.place_agent(iv, (x, y))

        # Create conveyors
        for l in range(len(conveyors)):
            no = l + no + 1
            cv = Conveyor(no, self)
            self.schedule.add(cv)
            x, y = conveyors[l]
            self.grid.place_agent(cv, (x, y))

        # Some metrics we'll measure about our model
        self.datacollector = DataCollector(
            model_reporters={"Total Output": total_output},
            agent_reporters={"Pos": "pos"},
        )

    def step(self):
        """Runs a single tick of the clock in our simulation."""
        self.datacollector.collect(self)
        self.schedule.step()
        steps = self.schedule.steps

        if steps == 3000:
            print("output =", steps)
            print("output =", output)
            print("working_steps =", working_steps)
            print("working_counts =", working_counts)
            print("-------------------------------------------------------")
            self.running = False
