import Player
from AI.Tree import Tree


class AlphaBeta:
    def __init__(self, maximize_player: Player, game_tree: Tree):
        self.maximize_player = maximize_player
        self.game_tree = game_tree

        self.current_node = None

    def run(self):
        return