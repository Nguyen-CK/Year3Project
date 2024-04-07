import pygame
from pygame import display

from Game_Board import Square, Board, Box, Arrow
from Game_Board.Direction import Direction
import Player
from Pieces import Pebble

pygame.init()

screen_width = 1200
screen_height = 720

screen = pygame.display.set_mode((screen_width, screen_height))
running = True

player_1 = Player.Player(1)
player_2 = Player.Player(2)

# test_square = Square.Square(300, 250, 1, 1,100, player_1)
# test_arrow = Arrow.Arrow(300, 250, 1, Direction.LEFT)

# Attributes for a Tile
starting_x_position = screen_width // 6
starting_y_position = screen_height // 3
side = screen_width // 10

# top_row = []
# bottom_row = []

# test_pebble_1 = Pebble.Pebble(300, 350, 30)
# test_pebble_2 = Pebble.Pebble(400, 450, 20)
# test_box = Box.Box(100, 100, 50)

board = Board.Board(starting_x_position, starting_y_position, side)


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
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            if event.button == 1:
                # mouse_coord = f"x: {mx}    y: {my}"
                # print(mouse_coord)
                result = board.handle_click(mx, my)
                direction = result[0]
                square = result[1]

                if direction is not None and square is not None:
                    moved = board.full_move(square, direction)
                    if moved[1]:
                        cap_score = board.capture(moved[2], moved[3], moved[4])
                        print(f"Score: {cap_score}")
                        get_turn().add_score(cap_score)

                    #player = get_turn()
                    end_turn()
                    if board.check_row_empty():
                        board.refill_row(get_turn())

    if board.is_game_over():
        player_1.add_score(board.clear_row(player_1))
        player_2.add_score(board.clear_row(player_2))
    # screen.fill("white")

    draw(screen)

pygame.quit()
