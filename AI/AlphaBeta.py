import Player
from AI import Node
from Game_Board import Square, Direction


class AlphaBeta:
    """
    An AI class that uses Alpha-beta pruning algorithm to search for the best move
    Attributes:
    maximize_player (Player): The AI player, one that need to get moves to win for
    current_node (Node): The current state of the Game
    """
    def __init__(self, maximize_player: Player, root_node: Node):
        self.maximize_player = maximize_player

        self.current_node = root_node

    def run(self, node: Node, depth: int, iters: int = 0, alpha: int = float('-inf'), beta: int = float('inf')):
        """
        Run the algorithm to find the best move, stop when it reaches the end of the game or the desired depth
        Alpha-beta pruning will "prune" of the branch if alpha >= beta (unconsidered moves)
        :param node: the state of the game
        :param depth: how many turns ahead should be searched for
        :param iters: number of search it did
        :param alpha: best move found so far for maximizing player
        :param beta: best move found so far for minimizing player
        :return: node: the best move
                 iter: number of search
        """
        if node.is_terminal() or depth == 0:
            return node, iters

        best_node = None

        if node.board.turn == self.maximize_player.num:
            """
            MAXIMIZING
            """
            max_value = float('-inf')

            node.get_all_possible_moves()

            for child in node.children:
                result_node, iters = self.run(child, depth - 1, iters + 1, alpha, beta)
                value = result_node.value

                if value > max_value:
                    max_value = value
                    best_node = result_node

                alpha = max(alpha, max_value)
                if alpha >= beta:
                    break

            return best_node, iters
        else:
            """
            MINIMIZING
            """
            min_value = float('inf')

            node.get_all_possible_moves()

            for child in node.children:
                result_node, iters = self.run(child, depth - 1, iters + 1, alpha, beta)
                value = result_node.value

                if value < min_value:
                    min_value = value
                    best_node = result_node

                beta = min(beta, min_value)

                if alpha >= beta:
                    break

            return best_node, iters

    def update_current_node(self, tile: Square, direction: Direction):
        """
        Updates the current state of the Game in the AI
        :param tile: tile to move from
        :param direction: direction to move to
        :return:
        """
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
        """
        Back tracking the trace to find the move to play from the current state of the Game
        :param node: best move found in the tree
        :param play_move: move to play from the current state
        :param iterations: traces of the backtrack
        :return: the move to play from the current state
        """
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
