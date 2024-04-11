from Game_Board import Board, Square
from Game_Board.Direction import Direction
import Player
import copy


class Node:
    def __init__(self, board: Board, player_1: Player, player_2: Player,
                 tile: Square = None, direction: Direction = None, parent=None):
        self.board = board
        self.player_1 = player_1
        self.player_2 = player_2

        self.value = 0

        self.move = (tile, direction)
        self.parent = parent

        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def get_all_possible_moves(self):
        # for row in self.board.row_matrix:
        row = None
        print(f"########### Start Turn: {self.board.turn}")
        if self.board.turn == 1:
            row = self.board.row_matrix[1]
        elif self.board.turn == 2:
            row = self.board.row_matrix[0]
        else:
            return

        for tile in row:
            if tile.pebble_stored == 0:
                continue
            for direction in Direction:
                child = self.generate_node(tile, direction, self)
                if child not in self.children and child is not None:
                    self.add_child(child)

            """
            print("Move Right In NODE +++++++++++++++++++++++")
            print(f"Current Tile: {tile.rel_x}, {tile.rel_y} | Pebbles: {tile.pebble_stored}")
            # print(f"Previous Tile: {tile.rel_x}, {tile.rel_y}")
            for_right = copy.deepcopy(tile)
            for_left = copy.deepcopy(tile)
            right = self.generate_node(tile, Direction.RIGHT, self)
            print(f"Player 1: {right.player_1.score}     |  Player 2: {right.player_2.score}")
            if right not in self.children and right is not None:
                self.add_child(right)
            print("Move Left In NODE -----------------------")
            print(f"Current Tile: {tile.rel_x}, {tile.rel_y} | Pebbles: {tile.pebble_stored}")

            # print(f"Previous Tile: {tile.rel_x}, {tile.rel_y}")

            left = self.generate_node(tile, Direction.LEFT, self)
            print(f"Player 1: {left.player_1.score}     |  Player 2: {left.player_2.score}")
            if left not in self.children and left is not None:
                self.add_child(left)
            """
    def generate_node(self, tile: Square, direction: Direction, parent):
        new_board: Board = copy.deepcopy(self.board)
        if new_board.is_game_over():
            return None

        copy_tile = copy.deepcopy(tile)
        copy_player_1 = copy.deepcopy(self.player_1)
        copy_player_2 = copy.deepcopy(self.player_2)

        moved = new_board.full_move(copy_tile, direction)
        if moved[1]:
            cap_score = new_board.capture(moved[2], moved[3], moved[4])
            self.get_turn(new_board, copy_player_1, copy_player_2).add_score(cap_score)
        new_board.end_turn()
        print(f"=================End Turn -> {new_board.turn}")
        if new_board.check_row_empty():
            new_board.refill_row(self.get_turn(new_board, copy_player_1, copy_player_2))

        if new_board.is_game_over():
            copy_player_1.add_score(new_board.clear_row(copy_player_1))
            copy_player_2.add_score(new_board.clear_row(copy_player_2))

        return Node(new_board, copy_player_1, copy_player_2, copy_tile, direction, parent)

    def get_turn(self, board, player_1, player_2):
        if board.turn == 1:
            return player_1
        elif board.turn == 2:
            return player_2
        else:
            return None

    def is_terminal(self):
        return self.board.is_game_over()

    def set_value(self, maximizing_player: Player):
        if maximizing_player == self.player_1:
            self.value = self.player_1.score - self.player_2.score
        elif maximizing_player == self.player_2:
            self.value = self.player_2.score - self.player_1.score
