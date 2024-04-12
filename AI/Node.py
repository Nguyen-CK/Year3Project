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
        # print(f"########### Start Turn: {self.board.turn}")
        if self.board.turn == 1:
            row = self.board.row_matrix[1]
        elif self.board.turn == 2:
            row = self.board.row_matrix[0]
        else:
            return
        move = 0
        for tile in row:
            if tile.pebble_stored == 0:
                continue
            for direction in Direction:
                move += 1

                print(f"ºººººººººººººººMOVE: {move}ºººººººººººººººººººººººººº")
                if direction == Direction.RIGHT:
                    print("Move Right In NODE +++++++++++++++++++++++")
                else:
                    print("Move Left In NODE -----------------------")
                print(f"From: {self.board.__str__()}")
                print(f"Current Tile: {tile.rel_x}, {tile.rel_y} | Pebbles: {tile.pebble_stored}")

                tile_x = tile.rel_x
                tile_y = tile.rel_y
                child = self.generate_node(tile_x, tile_y, direction, self)
                print(f"Moved to: {child.board.__str__()}")
                print(f"Player 1: {child.player_1.score}     |  Player 2: {child.player_2.score}")
                print(f"Node value: {child.player_2.score - child.player_1.score}")
                print("-------------------------------------------------------------------")
                if child not in self.children and child is not None:
                    self.add_child(child)

    def generate_node(self, tile_x, tile_y, direction: Direction, parent):
        new_board: Board.Board = copy.deepcopy(self.board)
        # new_board: Board = parent.board
        if new_board.is_game_over():
            return None

        tile = new_board.get_square_from_pos(tile_x, tile_y)
        copy_player_1 = copy.deepcopy(self.player_1)
        copy_player_2 = copy.deepcopy(self.player_2)

        #print("------------MOVED IN NODE---------------")
        #print(new_board.__str__())

        moved = new_board.full_move(tile, direction)
        if moved[1]:
            cap_score = new_board.capture(moved[2], moved[3], moved[4])
            self.get_turn(new_board, copy_player_1, copy_player_2).add_score(cap_score)
        new_board.end_turn()
        #print(f"=================End Turn -> {new_board.turn}")
        if new_board.check_row_empty():
            new_board.refill_row(self.get_turn(new_board, copy_player_1, copy_player_2))

        if new_board.is_game_over():
            copy_player_1.add_score(new_board.clear_row(copy_player_1))
            copy_player_2.add_score(new_board.clear_row(copy_player_2))

        return Node(new_board, copy_player_1, copy_player_2, tile, direction, parent)

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

    def is_end(self):
        return len(self.children) == 0
