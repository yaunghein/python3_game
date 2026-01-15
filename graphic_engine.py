import pygame


class GraphicsEngine:
    def __init__(self, width, height):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Survival: Blue Circles vs Purple Squares")
        self.clock = pygame.time.Clock()
        self.font_large = pygame.font.SysFont("Arial", 72, bold=True)
        self.font_small = pygame.font.SysFont("Arial", 24)

    def start_frame(self):
        self.screen.fill((20, 20, 20))

    def render_circle(self, x, y, radius, color):
        pygame.draw.circle(self.screen, pygame.Color(
            color), (int(x), int(y)), radius)

    def render_square(self, x, y, size, color):
        rect = pygame.Rect(int(x - size), int(y - size), size * 2, size * 2)
        pygame.draw.rect(self.screen, pygame.Color(color), rect)

    def render_text(self, text, size="large"):
        font = self.font_large if size == "large" else self.font_small
        color = (255, 255, 255) if size == "small" else (255, 50, 50)
        surf = font.render(text, True, color)
        rect = surf.get_rect(
            center=(self.width//2, self.height//2 + (50 if size == "small" else 0)))
        self.screen.blit(surf, rect)

    def show_frame(self, fps):
        pygame.display.flip()
        self.clock.tick(fps)
