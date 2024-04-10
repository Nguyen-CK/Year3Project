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
        self.score += score

    def borrow_pebble(self):
        self.score -= 5
        return 5

    def display_score(self, screen):
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
