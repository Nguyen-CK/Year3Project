import copy

import Player
from AI import Node
from Game_Board import Board, Square, Direction

player_2 = Player.Player(3, 0)
player_1 = Player.Player(1, 0)

maximizing_player = copy.copy(player_2)

def play_turn(tile: Square, direction: Direction, board: Board):
    moved = board.full_move(tile, direction)
    if moved[1]:
        cap_score = board.capture(moved[2], moved[3], moved[4])
        print(f"Score: {cap_score}")
        get_turn(board).add_score(cap_score)

    board.end_turn()
    if board.check_row_empty():
        board.refill_row(get_turn(board))

def get_turn(board):
    if board.turn == 1:
        return player_1
    elif board.turn == 2:
        return player_2
    else:
        return None


board_test = Board.Board(0, 0, 10)

node = Node.Node(board_test, player_1, player_2)

node.set_value(maximizing_player)
node.get_all_possible_moves()

new_board = copy.deepcopy(board_test)
tile = new_board.get_square_from_pos(0,1)
copy_tile = copy.deepcopy(tile)

node.children[0].set_value(maximizing_player)
print("VALUE OF MOVE ! çççççççççççççççç")
print(node.children[0].value)
print(node.children[0].player_1.score)
print(node.children[0].player_2.score)
print(node.children[0].is_end())
print(node.is_end())

#print(new_board.__str__())
#play_turn(copy_tile, Direction.Direction.LEFT,new_board)
#print(new_board.__str__())
