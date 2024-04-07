import pygame
from Pieces import Stone

border_thickness = 1
color = (0, 0, 0)


class Box:

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
        return True if self.stone is None else False

    def is_empty(self):
        if self.no_stone() and self.pebble_stored == 0:
            return True
        else:
            return False

    def add_pebble(self):
        self.pebble_stored += 1

    def remove_stone(self):
        self.stone = None

    def capture_box(self):
        value = self.pebble_stored
        if self.stone is not None:
            value += self.stone.value

        self.pebble_stored = 0
        self.remove_stone()

        return value

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
