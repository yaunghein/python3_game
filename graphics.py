import pygame
from pygame import Vector2
from characters import Player


class GraphicsEngine:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((500, 500))

    def start_frame(self):
        self.screen.fill("purple")

    def show_frame(self):
        pygame.display.flip()

    def render_circle(self, origin: Vector2, radius, color):
        pygame.draw.circle(self.screen, color, origin, radius)
    
    def render_player(self, player: Player):
        pygame.draw.circle(self.screen, player.color, player.pos, player.radius)

        # Bullet launch hole / orientation indicator
        offset = Vector2(player.radius * 0.75)
        
        pygame.draw.circle(self.screen, "black")
