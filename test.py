import copy
import time

import Player
from AI import Node, Tree, MiniMax
from Game_Board import Board, Square, Direction

player_2 = Player.Player(2, 0)
player_1 = Player.Player(1, 0)

maximizing_player = copy.copy(player_1)

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

node = Node.Node(board_test, player_1, player_2, maximizing_player)

#node.set_value(maximizing_player)
#node.get_all_possible_moves()

new_board = copy.deepcopy(board_test)
tile = new_board.get_square_from_pos(0,1)
copy_tile = copy.deepcopy(tile)


tree = Tree.Tree(new_board, player_1, player_2, maximizing_player)
# tree.build_tree(tree.root, 4)

minimax = MiniMax.MiniMax(maximizing_player, node)

# print(f"Current Board: \n {minimax.current_node.board.__str__()}")
# minimax.update_current_node(tile, Direction.Direction.LEFT)
# print(f"Current Board: \n {minimax.current_node.board.__str__()}")
start = time.time()
result = minimax.run(node, 5)
end = time.time()
#parent = result[0]
move_node = result[0]
iterations = result[1]
# moves = result[2]
play_move = minimax.get_play_move(move_node)
move_square = play_move.move[0]
move_direction = play_move.move[1]
print(minimax.current_node.__str__())
print(f"BEFORE UPDATE---------\n PARENT: {minimax.current_node.parent}")
minimax.update_current_node(move_square, move_direction)

square = move_node.move[0]
direction = move_node.move[1]
#print(moves) #.board.__str__())
#print(node.board.__str__())
#print("--------------------------------")
#print(f"Square: {move_square.__str__()} | Direction: {move_direction.__str__()}")
#print(play_move.board.__str__())
#print(f"PARENT NODE: {move_node.parent.board.__str__()}")
#print(f"BEST MOVE: {move_node.board.__str__()}")
#print(f"Player 1: {move_node.player_1.score} | Player 2: {move_node.player_2.score}")
#print(move_node.value)
print(f"Iterations: {iterations} | Time: {end - start}")
print(minimax.current_node.__str__())
print(f" PARENT: {minimax.current_node.parent}")



#print(new_board.__str__())
#play_turn(copy_tile, Direction.Direction.LEFT,new_board)
#print(new_board.__str__())
