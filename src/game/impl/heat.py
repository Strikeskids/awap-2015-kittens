from .main import MainPlayer
from collections import deque

class HeatPlayer(MainPlayer):
	def gaussian(self, x):
		v = 1 / (sqrt(ORDER_VAR * 2 * pi)) * e**(-x**2/(2*ORDER_VAR))

		return v

	def push_heat(self, loc):
		queue = deque()
		queue.addleft(loc)
		queue.addleft(-1)
		processed = set()

		d = 0
		limit = float("inf") # change me

		eval_func = self.gaussian

		while len(queue) > 1
			cur = queue.pop()
			if cur in processed:
				continue
			if cur == -1:
				d += 1
				if d > limit:
					break
				queue.append(-1)
				continue
			processed.add(cur)
			self.graph.node[cur]["heat"] += eval_func(d)
			queue.extendleft(self.graph.neighbors(cur))

	def clear_heat(self, loc):
		queue = deque()
		queue.addleft(loc)
		queue.addleft(-1)
		processed = set()

		d = 0
		limit = float("inf") # change me

		eval_func = lambda x: 1 - (self.gaussian / sqrt(2 * pi * ORDER_VAR))

		while len(queue) > 1
			cur = queue.pop()
			if cur in processed:
				continue
			if cur == -1:
				d += 1
				if d > limit:
					break
				queue.append(-1)
				continue
			processed.add(cur)
			self.graph.node[cur]["heat"] *= eval_func(d)
			queue.extendleft(self.graph.neighbors(cur))