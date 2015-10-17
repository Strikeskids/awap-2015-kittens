from .main import MainPlayer
from collections import deque

class BFSPlayer(MainPlayer):
	def update_stations(self, new_loc):
		queue = deque()
		queue.extendleft(stations)
		queue.addleft(-1)
		processed = set()
		groups = [[]]

		d = 0
		limit = float("inf") # change me

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
			self.graph.node[cur]["dist"] = d
			self.graph.node[cur]["value"] = 1
			groups[-1].append(cur)
			queue.extendleft(self.graph.neighbors(cur))

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