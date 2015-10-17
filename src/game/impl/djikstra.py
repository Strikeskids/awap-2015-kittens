from .main import MainPlayer
from ..settings import *

from heapq import heappush, heappop, heapify

class DjikstraPlayer(MainPlayer):
    PRICE_CONSTANT = 0.5
    PRICE_LEVEL = 30

    def evaluate_order(self, state, order):
        step_distance = self.PRICE_CONSTANT * DECAY_FACTOR
        cost_maximum = self.PRICE_CONSTANT * order.get_money() + PRICE_LEVEL

        closed = dict()
        q = [(0, x, None) for x in self.stations]

        heapify(q)

        while q:
            current_distance, current_node, previous_node = heappop(q)

            if current_node in closed: continue
            closed[current_node] = previous_node
            if current_node == order.node: break

            for adj in self.graph.neighbors(current_node):
                if adj in closed: continue
                if state.graph[current_node][adj]['in_use']: continue

                weight = self.graph[current_node][adj]['weight']
                distance = current_distance + weight + step_distance
                if distance > cost_maximum: continue

                heappush(q, (distance, adj, current_node))

        if order.node not in closed: return

        path = [order.node]
        while path[-1]:
            path.append(closed[path[-1]])

        del path[-1]
        path.reverse()

        return path
