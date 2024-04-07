import pygame

border_thickness = 2
color = (0, 0, 0)  # black


class Pebble:
    def __init__(self, x_position, y_position, radius):
        self.x_position = x_position
        self.y_position = y_position
        self.radius = radius
        self.value = 1

    def draw(self, screen):
        pygame.draw.circle(screen, color, (int(self.x_position), int(self.y_position)), int(self.radius), border_thickness)
