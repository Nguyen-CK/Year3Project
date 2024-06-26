from Game_Board import Board, Square
from Game_Board.Direction import Direction
import Player
import copy


class Node:
    """
    A class representing a Node, the state of the game
    Attributes:
    board (Board): the state of the game in the Node
    player_1 (Player): player 1 in the game
    player_2 (Player): player 2 in the game
    maximizing_player (Player): player who is the AI
    value (float): the value of the node
    tile (Square): the tile that it moved from to get to this node
    direction (Direction): the direction that it moved from to get to this node
    move ((Square), (Direction)): the move to get to this node
    parent (Node): the parent of the node
    children (list[Node]): the children of this node
    """

    def __init__(self, board: Board, player_1: Player, player_2: Player, maximizing_player: Player,
                 tile: Square = None, direction: Direction = None, parent=None):
        self.board = board
        self.player_1 = player_1
        self.player_2 = player_2

        self.maximizing_player = maximizing_player

        self.value = self.set_value(maximizing_player)

        self.move = (tile, direction)
        self.parent = parent

        self.children = []

    def add_child(self, child):
        """
        Adds a child to the Node
        :param child: node to add
        :return:
        """
        self.children.append(child)

    def get_all_possible_moves(self):
        """
        Play all possible move from the current node
        :return:
        """
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
                """
                ###############DEBUG####################
                print(f"ºººººººººººººººMOVE: {move}ºººººººººººººººººººººººººº")
                if direction == Direction.RIGHT:
                    print("Move Right In NODE +++++++++++++++++++++++")
                else:
                    print("Move Left In NODE -----------------------")
                print(f"From: {self.board.__str__()}")
                print(f"Current Tile: {tile.rel_x}, {tile.rel_y} | Pebbles: {tile.pebble_stored}")
                """
                tile_x = tile.rel_x
                tile_y = tile.rel_y
                child = self.generate_node(tile_x, tile_y, direction, self)
                """
                print(f"Moved to: {child.board.__str__()}")
                print(f"Player 1: {child.player_1.score}     |  Player 2: {child.player_2.score}")
                print(f"Node value: {child.player_2.score - child.player_1.score}")
                print("-------------------------------------------------------------------")
                """
                if child not in self.children and child is not None:
                    self.add_child(child)

    def generate_node(self, tile_x, tile_y, direction: Direction, parent):
        """
        Generate a node from the given move
        :param tile_x: x coordinate of the tile to move from
        :param tile_y: y coordinate of the tile to move from
        :param direction: direction to move to
        :param parent: parent of the node
        :return: newly state of the game from the move (Node)
        """
        new_board: Board.Board = copy.deepcopy(self.board)
        # new_board: Board = parent.board
        if new_board.is_game_over():
            return None

        tile = new_board.get_square_from_pos(tile_x, tile_y)
        copy_player_1 = copy.deepcopy(self.player_1)
        copy_player_2 = copy.deepcopy(self.player_2)

        # print("------------MOVED IN NODE---------------")
        # print(new_board.__str__())

        moved = new_board.full_move(tile, direction)
        if moved[1]:
            cap_score = new_board.capture(moved[2], moved[3], moved[4])
            self.get_turn(new_board, copy_player_1, copy_player_2).add_score(cap_score)
        new_board.end_turn()
        # print(f"=================End Turn -> {new_board.turn}")
        if new_board.check_row_empty():
            new_board.refill_row(self.get_turn(new_board, copy_player_1, copy_player_2))

        if new_board.is_game_over():
            copy_player_1.add_score(new_board.clear_row(copy_player_1))
            copy_player_2.add_score(new_board.clear_row(copy_player_2))

        # print(f"Moving from: {tile.rel_x}, {tile.rel_y} with {direction}")

        return Node(new_board, copy_player_1, copy_player_2, self.maximizing_player, tile, direction, parent)

    def get_turn(self, board, player_1, player_2):
        """
        Get the current player's in the turn
        :param board: the game board
        :param player_1:
        :param player_2:
        :return: the player of the current turn
        """
        if board.turn == 1:
            return player_1
        elif board.turn == 2:
            return player_2
        else:
            return None

    def is_terminal(self):
        """
        Check if the game is over in this state
        :return:
        """
        return self.board.is_game_over()

    def set_value(self, maximizing_player: Player):
        """
        Set the value of the Node
        :param maximizing_player: player who is the AI
        :return: value of the node
        """
        if maximizing_player == self.player_1:
            return self.player_1.score - self.player_2.score
        elif maximizing_player == self.player_2:
            return self.player_2.score - self.player_1.score
        else:
            return 0

    def is_end(self):
        """
        Check if the node is a leaf node
        :return:
        """
        return len(self.children) == 0

    def __str__(self):
        return (f"------------------Node---------------------\n "
                f"Board: {self.board.__str__()}\n Tile move: {self.move[0]}     | Direction: {self.move[1]} \n "
                f"Player 1: {self.player_1.score} | Player 2: {self.player_2.score}\n Value: {self.value}")
