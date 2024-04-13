import Player
from AI import Node


class AlphaBeta:
    def __init__(self, maximize_player: Player, root_node: Node):
        self.maximize_player = maximize_player

        self.current_node = root_node

    def run(self):
        return