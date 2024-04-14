import pygame

from Game_Board.Direction import Direction


class Arrow:
    """
    A class to create GUI arrows for the user to play the game
    Attributes:
        direction (Direction): direction of the Arrow
        x1 (int): x position of the first vertice
        y1 (int): y position of the first vertice
        x2 (int): x position of the second vertice
        y2 (int): y position of the second vertice
        x3 (int): x position of the third vertice
        y3 (int): y position of the third vertice
        player (Player): player of the Arrow
    """
    def __init__(self, x, y, player, direction: Direction):
        self.x1 = x
        self.y1 = y

        self.point_1 = (self.x1, self.y1)

        self.x2 = x
        if player == 1:
            self.y2 = y + 100
        else:
            self.y2 = y - 100

        self.point_2 = (self.x2, self.y2)

        self.direction = direction

        self.y3 = (self.y1 + self.y2) / 2
        if direction == Direction.RIGHT:
            self.x3 = x + 100
        else:
            self.x3 = x - 100

        self.point_3 = (self.x3, self.y3)
        self.player = player

    def draw(self, screen):
        """
        Draws the Arrow on the screen
        :param screen: screen to draw the Arrow
        :return:
        """
        pygame.draw.polygon(screen, (0, 0, 0), (self.point_1, self.point_2, self.point_3), 2)

    def handle_click(self):
        """
        Handles when the user clicks on the Arrow
        :return: the Direction to move
        """
        return self.direction

    def is_in_bound(self, mx, my):
        """
        Checks if the mouse clicks on the Arrow
        :param mx: mouse x position
        :param my: mouse y position
        :return: True if the mouse clicks on the Arrow, False otherwise
        """
        boundary = self.get_bounds()
        starting_vertice = boundary[0]
        opposite_vertice = boundary[1]

        if self.direction == Direction.RIGHT:
            if self.player == 1:
                if starting_vertice[0] <= mx <= opposite_vertice[0] and starting_vertice[1] <= my <= opposite_vertice[1]:
                    return True
            else:
                if starting_vertice[0] <= mx <= opposite_vertice[0] and starting_vertice[1] >= my >= opposite_vertice[1]:
                    return True
        else:
            if self.player == 1:
                if starting_vertice[0] >= mx >= opposite_vertice[0] and starting_vertice[1] <= my <= opposite_vertice[1]:
                    return True
            else:
                if starting_vertice[0] >= mx >= opposite_vertice[0] and starting_vertice[1] >= my >= opposite_vertice[1]:
                    return True

        return False

    def get_bounds(self):
        """
        Returns the boundaries of the Arrow
        :return: top left, bottom right of the "square" encompassing the Arrow
        """
        starting_vertice = self.point_1  # starting vertice
        opposite_vertice = None

        if self.direction == Direction.RIGHT:
            opposite_vertice = (self.x2 + 100, self.y2)
        else:

            opposite_vertice = (self.x2 - 100, self.y2)

        return starting_vertice, opposite_vertice
