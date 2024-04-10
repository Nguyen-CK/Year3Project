import Player
from AI.Node import Node
from Game_Board import Board


class Tree:
    def __init__(self, board: Board, player_1: Player, player_2: Player):
        self.root = Node(board, player_1, player_2)

    def build_tree(self):
        self.generate_branches(self.root)

    def generate_branches(self, node: Node):
        if node.is_terminal():
            return

        node.get_all_possible_moves()
        for child in node.children:
            self.generate_branches(child)

        return
