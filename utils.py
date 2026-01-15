import pygame


class GameField:
    def __init__(self, x_min, y_min, x_max, y_max):
        self.x_min = x_min
        self.y_min = y_min
        self.x_max = x_max
        self.y_max = y_max

    def clamp(self, x, y):
        x_clamped = max(self.x_min, min(self.x_max, x))
        y_clamped = max(self.y_min, min(self.y_max, y))
        return (x_clamped, y_clamped, x != x_clamped, y != y_clamped)


class InputController:
    def get_pressed_keys(self):
        pygame.event.pump()
        return pygame.key.get_pressed()
