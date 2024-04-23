import time

import pygame
from pygame import display

from AI import MiniMax, Tree, Node, AlphaBeta
from Game_Board import Square, Board, Box, Arrow
from Game_Board.Direction import Direction
import Player

"""
MAIN PROGRAM FOR THE GAME "O AN QUAN"
The GUI is setup with pygame in here with all the variables

"""

pygame.init()
"""
--------------SCREEN SET UP--------------
"""
screen_width = 1200
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
running = True

"""
--------------GAME SETUP--------------
"""
# Creating PLayers
player_1 = Player.Player(1)
player_2 = Player.Player(2)

# Attributes for a Tile
starting_x_position = screen_width // 6
starting_y_position = screen_height // 3
side = screen_width // 10

# Create Board
board = Board.Board(starting_x_position, starting_y_position, side)

def end_turn():
    """
    This function end the turn of the Game(in board)
    :return: Nothing, only happens if the turn does not match up (ERROR)
    """
    if board.turn == 1:
        board.turn = 2
    elif board.turn == 2:
        board.turn = 1
    else:
        return


def get_turn():
    """
    This function returns the player of the current turn
    :return: player of the current turn
    """
    if board.turn == 1:
        return player_1
    elif board.turn == 2:
        return player_2
    else:
        return None


def play_turn(tile: Square, direction: Direction):
    """
    This function plays the turn with the given tile and direction: full move -> capture -> end turn -> refill if needed
    :param tile: Tile to move from
    :param direction: Direction to move to
    :return:
    """
    # print("ººººººººººººººTurn in playºººººººººººººººººº")
    # print(f"Move: {tile.__str__()} | {direction.__str__()}")
    moved = board.full_move(tile, direction)
    if moved[1]:
        cap_score = board.capture(moved[2], moved[3], moved[4])
        # print(f"Score: {cap_score}")
        get_turn().add_score(cap_score)

    board.end_turn()
    if board.check_row_empty():
        board.refill_row(get_turn())


def add_score(player: Player, score: int):
    """
    Adds a score to the Player
    :param player:  to add to
    :param score: score to add
    :return:
    """
    player.add_score(score)


def draw(display_screen):
    """
    Draws the board and updates the screen
    :param display_screen: Screen to draw to
    :return:
    """
    display_screen.fill("white")
    board.draw_board(display_screen)
    player_1.display_score(display_screen)
    player_2.display_score(display_screen)
    # test_arrow.draw(display_screen)
    pygame.display.update()


"""
#####DEBUG######
for row in board.row_matrix:
    for cell in row:
        string = f"abs_x: {cell.x}      abs_y: {cell.y}"
        stri = f"x: {cell.rel_x}      y: {cell.rel_y}"

        print(string)
        print(stri)
"""

total_time = 0  # time AI needed to play for the whole game
total_search = 0  # number of searches it need
turn = 0  # total turns of the game

while running:
    """
    PLAYER TURN
    """
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
                    turn += 1
                    # print("----------CURREN NODE-------------")
                    # print(testing_algorithm.current_node.__str__())
                    # print(board.__str__())

    if board.is_game_over():
        """
        CHECK if game is over, then clear the board before ending
        """
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

print(f"Turns: {turn}")
print(f"Total Iterations: {total_search}    | Total Time: {total_time}")
pygame.quit()
