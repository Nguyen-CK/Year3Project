import pygame
from Pieces import Stone

border_thickness = 1
color = (0, 0, 0)


class Box:
    """
    This class represents a box at the end of the game board
    Attributes:
        x (int): x position of the box
        y (int): y position of the box
        width (int): width of the box
        height (int): height of the box
        rect (pygame.Rect): the rectangle to draw
        stone (Stone): the stone in the Box
        pebble_stored (int): the pebble in the Box

    """
    def __init__(self, x_position, y_position, side):
        self.x = x_position
        self.y = y_position

        self.width = side
        self.height = side * 2
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        x_offset = self.width / 2
        y_offset = self.height / 3

        stone_x = self.x + x_offset
        stone_y = self.y + y_offset

        self.stone = Stone.Stone(stone_x, stone_y, 30)  ##### need to off_set
        self.pebble_stored = 0

    def draw(self, screen):
        """
        Draws the box on the screen
        :param screen: screen to draw to
        :return:
        """
        pygame.draw.rect(screen, color, self.rect, border_thickness)
        if self.stone is not None:
            self.stone.draw(screen)
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
        number_image = number_font.render(number_text, True, color, (255,255,255))

        margin_x = (self.width - 5 - number_image.get_width()) // 2
        margin_y = (self.height - 5 - number_image.get_height()) // 3

        text_x = self.x + 2 + margin_x
        text_y = self.y + 2 + 2*margin_y

        screen.blit(number_image, (text_x, text_y))

    def no_stone(self):
        """
        Checks if the Box has no Stone
        :return: True if the Board has no stone, False otherwise
        """
        return True if self.stone is None else False

    def is_empty(self):
        """
        Checks if the Box is empty
        :return: True if the Box is empty, False otherwise
        """
        if self.no_stone() and self.pebble_stored == 0:
            return True
        else:
            return False

    def add_pebble(self):
        """
        Adds a Pebble to the Box
        :return:
        """
        self.pebble_stored += 1

    def remove_stone(self):
        """
        Removes the Stone from the Box
        :return:
        """
        self.stone = None

    def capture_box(self):
        """
        Captures the Box
        :return: the points get from the Box
        """
        value = self.pebble_stored
        if self.stone is not None:
            value += self.stone.value

        self.pebble_stored = 0
        self.remove_stone()

        return value

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
