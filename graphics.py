import pygame
from pygame import Vector2


class GraphicsEngine:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))

    def start_frame(self):
        self.screen.fill("purple")

    def show_frame(self):
        pygame.display.flip()

    def render_circle(self, origin: Vector2, radius, color):
        pygame.draw.circle(self.screen, color, origin, radius)
