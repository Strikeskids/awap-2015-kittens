from .main import MainPlayer

class BFSPlayer(MainPlayer):
	def update_stations(self):
		queue = stations[:]
		queue.append(-1)
		processed = set()
		groups = [[]]

		d = 0
		limit = float("inf") # change me

		while len(queue) > 1
			cur = queue.pop(0)
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
			queue.extend(self.graph.neighbors(cur))

		for i in range(len(groups)-1, -1, -1):
			for node in groups[i]:
				neighbors = self.graph.neighbors(node)
				cnt = 0

				for nieghbor in neighbors:
					if self.graph.node[neighbor]["dist"] == i-1:
						cnt += 1

				for nieghbor in neighbors:
					if self.graph.node[neighbor]["dist"] == i-1:
						self.graph.node[neighbor]["value"] += self.graph.node[node]["value"]/cnt
						g.edge[node][neighbor]["weight"] = self.graph.node[node]["value"]/cnt
						g.edge[neighbor][node]["weight"] = self.graph.node[node]["value"]/cnt