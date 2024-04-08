from Game_Board import Board, Square
from Game_Board.Direction import Direction
import Player


class Node:
    def __init__(self, board: Board, player_1: Player, player_2: Player):
        self.board = board
        self.player_1 = player_1
        self.player_2 = player_2

        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def get_all_possible_moves(self):
        for row in self.board.row_matrix:
            for tile in row:
                right = self.generate_node(tile, Direction.RIGHT)
                self.children.append(right)

                left = self.generate_node(tile, Direction.LEFT)
                self.children.append(left)

    def generate_node(self, tile: Square, direction: Direction):
        new_board: Board = self.board.copy()
        moved = new_board.full_move(tile, direction)
        if moved[1]:
            cap_score = new_board.capture(moved[2], moved[3], moved[4])
            self.get_turn(new_board).add_score(cap_score)
        new_board.end_turn()
        if new_board.check_row_empty():
            new_board.refill_row(self.get_turn(new_board))

        return Node(new_board, self.player_1, self.player_2)

    def get_turn(self, board):
        if board.turn == 1:
            return self.player_1
        elif board.turn == 2:
            return self.player_2
        else:
            return None
