import Player
from AI import Tree, Node
from Game_Board import Square, Direction


class MiniMax:
    def __init__(self, maximize_player: Player, root_node: Node):
        self.maximize_player = maximize_player
        self.current_node = root_node

    def run(self, node: Node, depth: int, iters: int = 0):
        # trace = []
        if node.is_terminal() or depth == 0:
            return node, iters # , trace.extend(node)

        # best_move = None
        best_node = None

        # parent = None
        if node.board.turn == self.maximize_player.num:  # Maximizing if the Turn is of the Player
            #maximize = True
            # print("MAXIMIZING")
            max_value = float('-inf')

            node.get_all_possible_moves()

            for child in node.children:
                result_node, iters = self.run(child, depth - 1, iters + 1)
                val = result_node.value
                if val > max_value:
                    max_value = val
                    # best_move = move
                    best_node = result_node
            return best_node, iters # , trace.extend(best_node)

        else:  # Minimizing if the Turn is not of the Player
            #maximize = False
            #print("MINIMIZING")
            min_value = float('inf')

            node.get_all_possible_moves()

            for child in node.children:
                result_node, iters = self.run(child, depth - 1, iters + 1)
                val = result_node.value
                if val < min_value:
                    min_value = val
                    # best_move = move
                    best_node = result_node

            return best_node, iters  # , trace.extend(best_node)

    def update_current_node(self, tile: Square, direction: Direction):
        #print("UPDATING Current Node")
        move = (tile, direction)
        branch = 1
        for child in self.current_node.children:
            #print(f"IN CHILD: {branch}")
            #print(child.move[0].__str__(), child.move[1])
            #print(child.board.__str__())
            if child.move == move:
                #print(child.board.__str__())
                self.current_node = child
                self.current_node.parent = None
                break
            branch = branch + 1

    def get_play_move(self, node: Node, play_move=None, iterations=0):
        if node.parent is None:
            #print(f"BEGIN: {node.board.__str__()} | trace: {iterations}")
            return play_move
        else:
            """
            print(f"Tracing: {node.board.__str__()} | trace: {iterations}")
            print(f"Square: {node.move[0].__str__()} | Direction: {node.move[1].__str__()}")
            print(f"Player 1: {node.player_1.score} | Player 2: {node.player_2.score}")
            print(node.value)
            print("--------------------------------------------------------------")
            #"""
            return self.get_play_move(node.parent, node, iterations + 1)

