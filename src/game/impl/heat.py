from __future__ import print_function
from .main import MainPlayer
from collections import deque
from math import *
from ..settings import *
import sys

class HeatPlayer(MainPlayer):
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

    def clear_heat(self, loc):
        queue = deque()
        queue.appendleft(loc)
        queue.appendleft(-1)
        processed = set()
        length = 2

        d = 0
        limit = float("inf") # change me

        eval_func = lambda x: e ** (-x*x / (SCORE_MEAN / DECAY_FACTOR)**2)

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