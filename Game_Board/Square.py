import pygame
import random

from Pieces.Pebble import Pebble

border_thickness = 1
red = (255, 100, 100)
blue = (100, 100, 255)
highlight = (100, 255, 100)
black = (0, 0, 0)
white = (255, 255, 255)

pebble_radius = 5


class Square:
    """
    A class representing a Tile on a Game_Board
    Attributes:
        x (int): The x position of the tile
        y (int): The y position of the tile
        rel_x (int): The relative x position of the tile
        rel_y (int): The relative y position of the tile
        side (int): The length of a side of the tile
        player (Player): The player allowed to use the tile
        rect_fill (Rectangle): The tile
        rect_border (Rectangle): The border of the tile
        color (Color): The color of the tile
        pebble_stored (int): The pebble inside the tile
        is_highlighted (bool): Whether the tile is selected or not
    """

    def __init__(self, x_position, y_position, relative_x, relative_y, side, player):
        self.x = x_position
        self.y = y_position
        self.side = side

        self.rel_x = relative_x
        self.rel_y = relative_y

        self.rect_fill = pygame.Rect(x_position, y_position, side, side)
        self.rect_border = pygame.Rect(x_position, y_position,
                                       side, side)

        self.player = player
        if player == 1:
            self.color = red
        else:
            self.color = blue

        self.pebble_stored = 5
        self.is_highlighted = False

    def draw(self, screen):
        """
        Draws the square
        :param screen: the display of the game
        :return:
        """
        # rectangle fill
        if self.is_highlighted:
            pygame.draw.rect(screen, highlight, self.rect_fill)
        else:
            pygame.draw.rect(screen, self.color, self.rect_fill)
        pygame.draw.rect(screen, black, self.rect_border, border_thickness)  # border
        self.display_pebbles(self.pebble_stored, screen)

    def display_pebbles(self, pebbles, screen):
        """
        Displays the number of Pebbles in the Square
        :param pebbles: the array of Pebbles
        :param screen: the display of the game
        :return:
        """
        number_font = pygame.font.SysFont(None, 32)
        number_text = str(pebbles)
        if self.is_highlighted:
            number_image = number_font.render(number_text, True, black, highlight)
        else:
            number_image = number_font.render(number_text, True, black, self.color)

        margin_x = (self.side - 5 - number_image.get_width()) // 2
        margin_y = (self.side - 5 - number_image.get_height()) // 2

        text_x = self.x + 2 + margin_x
        text_y = self.y + 2 + margin_y

        screen.blit(number_image, (text_x, text_y))

    def get_boundaries(self):
        top_left = (self.x, self.y)
        top_right = (self.x + self.side, self.y)
        bottom_left = (self.x, self.y + self.side)
        bottom_right = (self.x + self.side, self.y + self.side)

        four_corners = [top_left, top_right, bottom_left, bottom_right]

        return four_corners

    def is_empty(self):
        return self.pebble_stored == 0

    def add_pebble(self):
        self.pebble_stored += 1

    def empty(self):
        self.pebble_stored = 0

    def capture_square(self):
        value = self.pebble_stored
        self.pebble_stored = 0

        return value

    def __eq__(self, other):
        return (self.rel_x == other.rel_x and self.rel_y == other.rel_y)

    def __str__(self):
        return f"Tile: {self.rel_x}, {self.rel_y} | {self.pebble_stored} pebbles"
