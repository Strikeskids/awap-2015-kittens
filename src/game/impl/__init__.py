from .main import MainPlayer
from .dijkstra import DijkstraPlayer
from .bfs import BFSPlayer
from .heat import HeatPlayer
from settings import *

class Player(DijkstraPlayer, HeatPlayer, MainPlayer, BFSPlayer):

	last_order_time=0

	def step(self, state):

        commands = []
        
        pending_orders = state.get_pending_orders()

       	if(state.get_money()>=INIT_BUILD_COST*BUILD_FACTOR**len(self.stations):
			station=self.findStation()
	        if(self.should_build_station(station)):  #Check if a new station should be built
	        	self.create_station(state,station)
	    	    commands.append(self.build_command(station))

        for order in pending_orders:
            if order.time_created > self.last_order_time:
                path=self.evaluate_order(state,order)
                self.last_order_time=order.time_created
                if path:
                	commands.append(self.send_command(order,path))
                	self.graph.node[path[0]]['production'] += order.get_money() - (len(path))*DECAY_FACTOR
                	break
               	else:
               		self.push_heat(order.node)

            else: break	        	

        return commands

    def findStation(self):
    	maxProb=self.hub.probs[0]["heat"]
    	ind=0

    	for i in range(len(self.hub_probs)):
    		if(self.graph.node[i]["heat"]>maxProb):
    			maxProb=self.graph.node[i]["heat"]
    			ind=1

    	return ind
