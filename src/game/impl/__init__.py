from .main import MainPlayer
from .dijkstra import DijkstraPlayer

class Player(DijkstraPlayer, MainPlayer):

	last_order_time=0

	def __init__(self, state):
		self.graph=state.get_graph()
		self.hub_probs = [0 for i in range(len(state.graph.node))]
        return

	def step(self, state):
        graph = state.get_graph()

        commands = []
        
        pending_orders = state.get_pending_orders()

        for i in range(len(pending_orders)-1, -1, -1):
            if pending_orders[i].time_created > self.last_order_time:
               self.propagate(pending_orders[i].node, state.graph)
            else: break
        
        self.last_order_time = pending_orders[-1].time_created

        if(True):  #Check if a new station should be built
	        station = self.findStation()
    	    commands.append(self.build_command(station))

        #Some function to find which orders to place 
        if(False):
        	commands.append(self.find_order())

        return commands

	def gaussian(self, x):
        v = 1 / (sqrt(ORDER_VAR * 2 * pi)) * e**(-x**2/(2*ORDER_VAR))

        #if x == 0:
        #    pass v += .5

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

    def findStation(self):
    	maxProb=0
    	ind=0
    	weights=[0 for i in range(len(self.hub_probs))]

    	for i in range(len(self.hub_probs)):
    		weights[i]=self.hub_probs[i]-self.station_probs[i]

    	for i in range(len(weights)):
    		if(weights[i]>maxProb):
    			maxProb=weights[i]
    			ind=i

    	return ind