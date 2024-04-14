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

# AI attributes
depth = 4
maximizing_player = player_1
root = Node.Node(board, player_1, player_2, maximizing_player)
"""
--------------AI CREATION--------------
NOTE: to use MiniMax AI uncomment line 49 and comment line 50 | to use Alpha-Beta AI do the reverse
"""
# testing_algorithm = MiniMax.MiniMax(maximizing_player, root)
testing_algorithm = AlphaBeta.AlphaBeta(maximizing_player, root)


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
    # """
    if board.turn == maximizing_player.num:
        """
        AI TURN
        """
        print("Running From Here!!!!")
        # print(testing_algorithm.current_node.board.__str__())
        # time.sleep(3)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        start_time = time.time()
        """
        AI search for best move
        """
        result = testing_algorithm.run(testing_algorithm.current_node, depth)
        move_node = result[0]  # best node found in the tree
        num_of_search = result[1]  # number of iterations it needed
        play_move = testing_algorithm.get_play_move(move_node)  # the move to do from the current turn
        end_time = time.time()

        time_pass = end_time - start_time  # time passed for AI to run

        play_tile = play_move.move[0]  # tile to move from
        direct = play_move.move[1]  # direction to move to
        """
        ###########DEBUG##############
        """
        # print("--------------------------------")
        # print(f"Tile: {play_tile.__str__()} | Direction: {direct.__str__()}")
        # print("--------------------------------")
        # print(f"MOVED TO: {play_move.board.__str__()}\n")
        print(f"Iterations: {num_of_search} | Time: {time_pass}\n")

        pos_x = play_tile.rel_x
        pos_y = play_tile.rel_y

        square = board.get_square_from_pos(pos_x, pos_y)
        """
        ###########DEBUG##############
        """
        # print(square, direct)
        # print(board.__str__())
        # print(f"Moving from: {square.rel_x}, {square.rel_y} with {direct}")

        play_turn(square, direct)
        """
        ###########DEBUG##############
        """
        # print(f"++++++++++++CURRENT BOARD++++++++++++++\n {board.__str__()}")
        # print("----------CURREN NODE-------------")
        # print(testing_algorithm.current_node.__str__())

        """
        UPDATE THE CURRENT NODE IN THE AI
        """
        testing_algorithm.update_current_node(square, direct)

        total_time += time_pass
        total_search += num_of_search
        turn += 1

    else:
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
                        testing_algorithm.update_current_node(square, direct)
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

print(f"Maximizing Player: {maximizing_player.num}")
print(f"With Depth: {depth}")
print(f"Turns: {turn}")
print(f"Total Iterations: {total_search}    | Total Time: {total_time}")
pygame.quit()
