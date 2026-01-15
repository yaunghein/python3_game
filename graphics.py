import pygame


class GraphicsEngine:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))

    def start_frame(self):
        self.screen.fill("purple")

    def show_frame(self):
        pygame.display.flip()

    def render_circle(self, x, y, radius, color):
        pygame.draw.circle(self.screen, color, pygame.Vector2(x, y), radius)
