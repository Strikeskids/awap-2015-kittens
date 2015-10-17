from ..base_player import BasePlayer
from ..settings import *

class MainPlayer(BasePlayer):
    def __init__(self, state):
        self.grapsh = state.graph
