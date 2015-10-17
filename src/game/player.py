from __future__ import print_function

from .settings import *
from .base_player import BasePlayer

from heapq import heappush, heappop, heapify
from collections import deque
from math import sqrt, e, pi
import traceback
import sys

class Player(BasePlayer):

    last_order_time=0

    last_heat_reset = 0

    PRICE_CONSTANT = 0.5
    PRICE_LEVEL = 30

    def __init__(self, state):
        self.graph = state.graph
        self.stations = []

        for i in range(len(self.graph.node)):
            self.graph.node[i]["heat"] = 0

            for n in self.graph.neighbors(i):
                self.graph.edge[i][n]["weight"] = 0
                self.graph.edge[n][i]["weight"] = 0

    def step(self, state):
        try:
            commands = []
            
            pending_orders = state.get_pending_orders()

            print("checking stations", file=sys.__stdout__)
            if state.get_money() >= INIT_BUILD_COST*BUILD_FACTOR**len(self.stations):
                station=self.findStation()
                if self.should_build_station(state, station):  #Check if a new station should be built
                    self.create_station(state,station)
                    commands.append(self.build_command(station))
                    print(commands, file=sys.__stdout__)

            print("checking orders", file=sys.__stdout__)
            for order in pending_orders:
                if order.time_created > self.last_order_time:
                    print("evaluating order", order, file=sys.__stdout__)
                    path=self.evaluate_order(state,order)
                    print("done evaluating", order, path, file=sys.__stdout__)
                    self.last_order_time = order.time_created
                    if path:
                        commands.append(self.send_command(order,path))
                        print(self.graph.node[path[0]], file=sys.__stdout__)
                        self.graph.node[path[0]]['production'] += order.get_money() - (len(path))*DECAY_FACTOR
                        break
                    else:
                        print("pushing heat", order.node, file=sys.__stdout__)
                        self.push_heat(order.node)
                        print("done pushing", order.node, file=sys.__stdout__)
            print("done", commands, file=sys.__stdout__)
            return commands
        except Exception as e:
            traceback.print_exc(file=sys.__stdout__)

    def findStation(self):
        maxProb=self.graph.node[0]["heat"]
        ind=0

        for i in range(len(self.graph.node)):
            if self.graph.node[i]["heat"] > maxProb and not self.graph.node[i]["is_station"]:
                maxProb=self.graph.node[i]["heat"]
                ind=i

        return ind

    def create_station(self, state, station):
        data = self.graph.node[station]
        data['production'] = 0
        data['created_time'] = state.get_time()
        data['created_heat_time'] = state.get_time() - self.last_heat_reset
        data['created_heat'] = data['heat']
        data['is_station'] = True

        print("CREATED STATION", station, file=sys.__stdout__)

        self.stations.append(station)
        print("updating stations", file=sys.__stdout__)
        self.update_stations()
        print("clearing heat", file=sys.__stdout__)
        self.clear_heat(state, station)
        print("done clearing heat", file=sys.__stdout__)

    def should_build_station(self, state, candidate):
        if len(self.stations) == 0:
            return state.get_time() > 25
        total_metric = 0
        for station in self.stations:
            data = self.graph.node[station]
            current_metric = data['production'] * data['created_heat_time'] \
                    / data['created_heat'] / self.graph.degree(station) \
                    / (state.get_time() - data['created_time'])
            total_metric += current_metric

        expected_production = total_metric / len(self.stations) \
            * self.graph.node[candidate]['heat'] \
            * (GAME_LENGTH - state.get_time()) * self.graph.degree(candidate)

        build_cost = INIT_BUILD_COST * BUILD_FACTOR ** len(self.stations)

        return state.get_money() > build_cost and expected_production > 2 * build_cost

    def update_stations(self):
        queue = deque()
        queue.extendleft(self.stations)
        queue.appendleft(-1)
        processed = set()
        groups = [[]]

        d = 0
        limit = float("inf") # change me

        while True:
            cur = queue.pop()
            if cur == -1:
                d += 1
                if d > limit:
                    break
                if not queue:
                    break
                queue.appendleft(-1)
                continue
            processed.add(cur)
            self.graph.node[cur]["dist"] = d
            self.graph.node[cur]["value"] = 1
            groups[-1].append(cur)
            for node in self.graph.neighbors(cur):
                if node not in processed:
                    queue.appendleft(node)
                    processed.add(node)

        for i in range(len(groups)-1, -1, -1):
            for node in groups[i]:
                neighbors = self.graph.neighbors(node)
                cnt = 0

                for neighbor in neighbors:
                    if self.graph.node[neighbor]["dist"] == i-1:
                        cnt += 1

                for neighbor in neighbors:
                    if self.graph.node[neighbor]["dist"] == i-1:
                        self.graph.node[neighbor]["value"] += self.graph.node[node]["value"]/cnt
                        self.graph.edge[node][neighbor]["weight"] = self.graph.node[node]["value"]/cnt
                        self.graph.edge[neighbor][node]["weight"] = self.graph.node[node]["value"]/cnt

    def evaluate_order(self, state, order):
        step_distance = self.PRICE_CONSTANT * DECAY_FACTOR
        cost_maximum = self.PRICE_CONSTANT * order.get_money() + self.PRICE_LEVEL

        closed = dict()
        q = [(0, x, None) for x in self.stations]

        print(self.stations, file=sys.__stdout__)

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

    def gaussian(self, x):
        v = 1 / (sqrt(ORDER_VAR * 2 * pi)) * e**(-x**2/(2*ORDER_VAR))

        return v

    def push_heat(self, loc):
        queue = deque()
        queue.appendleft(loc)
        queue.appendleft(-1)
        processed = set()
        length = 2

        d = 0
        limit = float("inf") # change me

        eval_func = self.gaussian

        while length > 1:
            #print(queue, file=sys.__stdout__)
            cur = queue.pop()
            length -=1
            if cur == -1:
                d += 1
                if d > limit:
                    break
                queue.appendleft(-1)
                length += 1
                continue
            processed.add(cur)
            self.graph.node[cur]["heat"] += eval_func(d)
            for node in self.graph.neighbors(cur):
                if node not in processed:
                    queue.appendleft(node)
                    processed.add(node)
                    length += 1

    def clear_heat(self, state, loc):
        self.last_heat_reset = state.get_time()
        for i in range(len(self.graph.node)):
            self.graph.node[i]["heat"] = 0

        return
        queue = deque()
        queue.appendleft(loc)
        queue.appendleft(-1)
        processed = set()
        length = 2

        d = 0
        limit = 10 # change me

        eval_func = lambda x:  0 + .1*x

        while length > 1:
            #print(queue, file=sys.__stdout__)
            cur = queue.pop()
            length -=1
            if cur == -1:
                d += 1
                if d > limit:
                    break
                queue.appendleft(-1)
                length += 1
                continue
            processed.add(cur)
            self.graph.node[cur]["heat"] *= eval_func(d)
            for node in self.graph.neighbors(cur):
                if node not in processed:
                    queue.appendleft(node)
                    processed.add(node)
                    length += 1

    def get_probs(self):
        return [self.graph.node[i]["heat"] for i in range(len(self.graph.node))]
