import pygame


class Player:
    """
    A class to represent a Player and hold information about it
    Attributes:
        num (int): The player number
        score (int): The player score
    """

    def __init__(self, num, score=0):
        self.num = num
        self.score = score

    def add_score(self, score):
        """
        Adds a score to the Player
        :param score: value to add
        :return:
        """
        self.score += score

    def borrow_pebble(self):
        """
        Take pebbles from the player
        :return:
        """
        self.score -= 5
        return 5

    def display_score(self, screen):
        """
        Displays the score of the player on the screen
        :param screen: screen to display to
        :return:
        """
        font = pygame.font.SysFont(None, 32)
        text = f"Player {self.num}:     {self.score}"

        text_print = font.render(text, True, (0, 0, 0), (255, 255, 255))
        text_x = 50
        text_y = 0
        if self.num == 1:
            text_y = 600
        elif self.num == 2:
            text_y = 100

        screen.blit(text_print, (text_x, text_y))

    def __eq__(self, other):
        return self.num == other.num
