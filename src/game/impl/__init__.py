from __future__ import print_function
from .main import MainPlayer
from .dijkstra import DijkstraPlayer
from .bfs import BFSPlayer
from .heat import HeatPlayer
from ..settings import *
import sys
import traceback

class Player(DijkstraPlayer, HeatPlayer, MainPlayer, BFSPlayer):

    last_order_time=0

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
        data['created_heat'] = data['heat']
        data['is_station'] = True

        print("CREATED STATION", station, file=sys.__stdout__)

        self.stations.append(station)
        print("updating stations", file=sys.__stdout__)
        self.update_stations()
        print("clearing heat", file=sys.__stdout__)
        self.clear_heat(station)
        print("done clearing heat", file=sys.__stdout__)

    def should_build_station(self, state, candidate):
        if len(self.stations) == 0:
            return state.get_time() > 25
        total_metric = 0
        for station in self.stations:
            data = self.graph.node[station]
            current_metric = data['production'] * data['created_time'] \
                    / data['created_heat'] / self.graph.degree(station) \
                    / (state.get_time() - data['created_time'])
            total_metric += current_metric

        expected_production = total_metric / len(self.stations) \
            * self.graph.node[candidate]['heat'] \
            * (GAME_LENGTH - state.get_time()) * self.graph.degree(candidate)

        build_cost = INIT_BUILD_COST * BUILD_FACTOR ** len(self.stations)

        return state.get_money() > build_cost and expected_production > 2 * build_cost

    def get_probs(self):
        return [self.graph.node[i]["heat"] for i in range(len(self.graph.node))]
