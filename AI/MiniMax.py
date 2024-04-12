import Player
from AI import Tree, Node
from Game_Board import Square, Direction


class MiniMax:
    def __init__(self, maximize_player: Player, game_tree: Tree):
        self.maximize_player = maximize_player
        self.game_tree = game_tree

        self.current_node = game_tree.root

    def run(self, node: Node, iters: int = 0):
        if node.is_terminal() or node.is_end():
            return node, iters

        # best_move = None
        best_node = None
        if node.board.turn == self.maximize_player.num:  # Maximizing if the Turn is of the Player
            maximize = True
            max_value = float('-inf')

            for child in node.children:
                result_node, iters = self.run(child, iters + 1)
                val = result_node.value
                if val > max_value:
                    max_value = val
                    # best_move = move
                    best_node = result_node
            return best_node, iters

        else:  # Minimizing if the Turn is not of the Player
            maximize = False
            min_value = float('inf')

            for child in node.children:
                result_node, iters = self.run(child, iters + 1)
                val = result_node.value
                if val < min_value:
                    min_value = val
                    # best_move = move
                    best_node = result_node

            return best_node, iters

    def update_current_node(self, tile: Square, direction: Direction):
        self.current_node = self.game_tree.traverse_node(self.current_node, tile, direction)
