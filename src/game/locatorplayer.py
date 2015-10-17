from __future__ import print_function
from base_player import BasePlayer
import logging as log
import networkx as nx
import random
from settings import *
from math import *

class Player(BasePlayer):
    
    has_built_station = False
    last_order_time = 0

    def __init__(self, state):
        self.hub_probs = [0 for i in range(len(state.graph.node))]
        return

    def path_is_valid(self, state, path):
        graph = state.get_graph()
        for i in range(0, len(path) - 1):
            if graph.edge[path[i]][path[i + 1]]['in_use']:
                return False
        return True

    def step(self, state):
        graph = state.get_graph()
        station = graph.nodes()[0]

        commands = []
        if not self.has_built_station:
            commands.append(self.build_command(station))
            self.has_built_station = True

        pending_orders = state.get_pending_orders()

        for i in range(len(pending_orders)-1, -1, -1):
            if pending_orders[i].time_created > self.last_order_time:
                self.propagate(pending_orders[i].node, state.graph)

        self.last_order_time = pending_orders[-1].time_created

        if len(pending_orders) != 0:
            order = random.choice(pending_orders)
            path = nx.shortest_path(graph, station, order.get_node())
            if self.path_is_valid(state, path):
                commands.append(self.send_command(order, path))

        return commands

    def gaussian(self, x):
        v = 1 / (sqrt(ORDER_VAR * 2 * pi)) * e**(-x**2/(2*ORDER_VAR))

        if x == 0:
            pass #v += .5

        return v

    def propagate(self, loc, graph):
        queue = [loc, -1]
        processed = set()
        d = 0
        eval_func = self.gaussian

        while len(queue) > 1:
            val = queue.pop(0)
            if val in processed:
                continue
            if val == -1:
                d += 1
                queue.append(-1)
                continue
            processed.add(val)
            self.hub_probs[val] += eval_func(d)
            queue.extend(graph.neighbors(val))

    def get_probs(self):
        return self.hub_probs