from ..base_player import BasePlayer
from ..settings import *

class MainPlayer(BasePlayer):
    def __init__(self, state):
        self.graph = state.graph
        self.stations = []

        for i in range(len(self.graph.node)):
        	self.graph.node[i]["heat"] = 0