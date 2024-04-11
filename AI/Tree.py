import copy

import Player
from AI.Node import Node
from Game_Board import Board, Square, Direction


class Tree:
    def __init__(self, board: Board, player_1: Player, player_2: Player, maximizing_player: Player):
        self.root = Node(copy.deepcopy(board), player_1, player_2)
        self.maximizing_player = maximizing_player

        self.root.set_value(maximizing_player)

    def build_tree(self):
        self.generate_branches(self.root)

    def generate_branches(self, node: Node):
        if node.is_terminal():
            return

        node.get_all_possible_moves()
        node.set_value(self.maximizing_player)
        for child in node.children:
            self.generate_branches(child)

        return

    def traverse_node(self, start_node: Node, tile: Square, direction: Direction):
        move = (tile, direction)
        for child in start_node.children:
            if child.move == move:
                return child
