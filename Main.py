import time

import pygame
from pygame import display

from AI import MiniMax, Tree
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
tree.build_tree(tree.root, 4)
# tree.generate_branches(tree.root)

testing_algorithm = MiniMax.MiniMax(maximizing_player, tree)


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
    moved = board.full_move(tile, direction)
    if moved[1]:
        cap_score = board.capture(moved[2], moved[3], moved[4])
        print(f"Score: {cap_score}")
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
while running:
    # """
    if board.turn == maximizing_player.num:
        print("Running From Here!!!!")
        time.sleep(3)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        start_time = time.time()

        result = testing_algorithm.run(testing_algorithm.current_node)
        move_node = result[0]
        num_of_search = result[1]

        end_time = time.time()

        square, direct = move_node.move
        print(board.__str__())
        print(f"Moving from: {square.rel_x}, {square.rel_y} with {direct}")
        play_turn(square, direct)
        testing_algorithm.update_current_node(square, direct)

        if testing_algorithm.current_node.is_end():
            testing_algorithm.game_tree.build_tree(testing_algorithm.current_node, 4)

    else:
        # """
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
                        # print(board.__str__())
                        """
                        moved = board.full_move(square, direction)
                        if moved[1]:
                            cap_score = board.capture(moved[2], moved[3], moved[4])
                            print(f"Score: {cap_score}")
                            get_turn().add_score(cap_score)
    
                        board.end_turn()
                        if board.check_row_empty():
                            board.refill_row(get_turn())
                        """
        # time.sleep(3)

    if board.is_game_over():
        player_1.add_score(board.clear_row(player_1))
        player_2.add_score(board.clear_row(player_2))
    # screen.fill("white")

    draw(screen)

pygame.quit()
