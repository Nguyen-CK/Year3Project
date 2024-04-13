import time

import pygame
from pygame import display

from AI import MiniMax, Tree, Node
from Game_Board import Square, Board, Box, Arrow
from Game_Board.Direction import Direction
import Player

pygame.init()

screen_width = 1200
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
running = True

player_1 = Player.Player(1)
player_2 = Player.Player(2)

# Attributes for a Tile
starting_x_position = screen_width // 6
starting_y_position = screen_height // 3
side = screen_width // 10

board = Board.Board(starting_x_position, starting_y_position, side)

# AI attributes
maximizing_player = player_2

tree = Tree.Tree(board, player_1, player_2, maximizing_player)
#tree.build_tree(tree.root, 4)
# tree.generate_branches(tree.root)
root = Node.Node(board, player_1, player_2, maximizing_player)

testing_algorithm = MiniMax.MiniMax(maximizing_player, root)


def end_turn():
    if board.turn == 1:
        board.turn = 2
    elif board.turn == 2:
        board.turn = 1
    else:
        return


def get_turn():
    if board.turn == 1:
        return player_1
    elif board.turn == 2:
        return player_2
    else:
        return None


def play_turn(tile: Square, direction: Direction):
    #print("ººººººººººººººTurn in playºººººººººººººººººº")
    #print(f"Move: {tile.__str__()} | {direction.__str__()}")
    moved = board.full_move(tile, direction)
    if moved[1]:
        cap_score = board.capture(moved[2], moved[3], moved[4])
        #print(f"Score: {cap_score}")
        get_turn().add_score(cap_score)

    board.end_turn()
    if board.check_row_empty():
        board.refill_row(get_turn())


def add_score(player: Player, score: int):
    player.add_score(score)


def draw(display_screen):
    display_screen.fill("white")
    board.draw_board(display_screen)
    player_1.display_score(display_screen)
    player_2.display_score(display_screen)
    # test_arrow.draw(display_screen)
    pygame.display.update()


"""
for row in board.row_matrix:
    for cell in row:
        string = f"abs_x: {cell.x}      abs_y: {cell.y}"
        stri = f"x: {cell.rel_x}      y: {cell.rel_y}"

        print(string)
        print(stri)
"""
# print(board.__str__())
# play_turn(board.get_square_from_pos(0,1), Direction.RIGHT)
# print(board.__str__())
total_time = 0
total_search = 0
while running:
    #"""
    if board.turn == maximizing_player.num:
        print("Running From Here!!!!")
        #print(testing_algorithm.current_node.board.__str__())
        #time.sleep(3)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        start_time = time.time()

        result = testing_algorithm.run(testing_algorithm.current_node, 4)
        move_node = result[0]
        num_of_search = result[1]
        play_move = testing_algorithm.get_play_move(move_node)
        end_time = time.time()

        time_pass = end_time - start_time

        play_tile = play_move.move[0]
        direct = play_move.move[1]
        #print("--------------------------------")
        #print(f"Tile: {play_tile.__str__()} | Direction: {direct.__str__()}")
        #print("--------------------------------")
        #print(f"MOVED TO: {play_move.board.__str__()}\n")
        print(f"Iterations: {num_of_search} | Time: {time_pass}\n")

        pos_x = play_tile.rel_x
        pos_y = play_tile.rel_y

        square = board.get_square_from_pos(pos_x, pos_y)
        # print(square, direct)
        # print(board.__str__())
        # print(f"Moving from: {square.rel_x}, {square.rel_y} with {direct}")
        play_turn(square, direct)
        #print(f"++++++++++++CURRENT BOARD++++++++++++++\n {board.__str__()}")
        #print("----------CURREN NODE-------------")
        #print(testing_algorithm.current_node.__str__())
        testing_algorithm.update_current_node(square, direct)

        total_time += time_pass
        total_search += num_of_search

    else:
    #    """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if event.button == 1:
                    # mouse_coord = f"x: {mx}    y: {my}"
                    # print(mouse_coord)
                    result = board.handle_click(mx, my)
                    direct = result[0]
                    square = result[1]

                    if direct is not None and square is not None:
                        play_turn(square, direct)
                        testing_algorithm.update_current_node(square, direct)
                        #print("----------CURREN NODE-------------")
                        #print(testing_algorithm.current_node.__str__())
                        # print(board.__str__())

    if board.is_game_over():
        player_1.add_score(board.clear_row(player_1))
        player_2.add_score(board.clear_row(player_2))
        running = False
        print(f"-----------------Game Over!-----------------")
        print(f"Player 1: {player_1.score}      | Player 2: {player_2.score}")


    # screen.fill("white")

    draw(screen)

if player_1.score > player_2.score:
    print("Player 1 wins!")

elif player_1.score < player_2.score:
    print("Player 2 wins!")
else:
    print("Draw!")

print(f"Total Iterations: {total_search}    | Total Time: {total_time}")
pygame.quit()
