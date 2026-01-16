import pygame
import random

# =======================
# Characters
# =======================

class Player:
    def __init__(self, x, y, speed_x=2, speed_y=2):
        self.x = x
        self.y = y
        self.speed_x = speed_x
        self.speed_y = speed_y

    def move(self, left, right, up, down, game_field):
        self.x += self.speed_x * right - self.speed_x * left
        self.y += self.speed_y * down - self.speed_y * up

        self.x, self.y, _, _ = game_field.clamp(self.x, self.y)


class NPC:
    def __init__(self, x, y, speed_x=1, speed_y=1, color="blue"):
        self.x = x
        self.y = y
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.color = color
        self.hit_timer = 0 # count time frame after hit

    def move(self, game_field):
        self.x += self.speed_x
        self.y += self.speed_y

        self.x, self.y, x_edge, y_edge = game_field.clamp(self.x, self.y)

        if x_edge:
            self.speed_x *= -1
        if y_edge:
            self.speed_y *= -1

# =======================
# Graphics Engine
# =======================

class GraphicsEngine:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))

    def start_frame(self):
        self.screen.fill("yellow")

    def show_frame(self):
        pygame.display.flip()

    def render_circle(self, x, y, radius, color):
        pygame.draw.circle(
            self.screen,
            color,
            pygame.Vector2(x, y),
            radius
        )


# =======================
# Game Field
# =======================

class GameField:
    def __init__(self, x_min, y_min, x_max, y_max):
        self.x_min = x_min
        self.y_min = y_min
        self.x_max = x_max
        self.y_max = y_max

    def clamp(self, x, y):
        x_edge = False
        y_edge = False

        if x < self.x_min or x > self.x_max:
            x_edge = True
        if y < self.y_min or y > self.y_max:
            y_edge = True

        x = max(self.x_min, min(self.x_max, x))
        y = max(self.y_min, min(self.y_max, y))

        return x, y, x_edge, y_edge


# =======================
# Game Engine
# =======================

player_r = 20
npc_r = 20


class GameEngine:
    def __init__(self, graph_engine, game_field, player, npcs, fps=60):
        self.graph_engine = graph_engine
        self.game_field = game_field
        self.player = player
        self.npcs = npcs
        self.fps = fps
        self.running = True

    def update_state(self, keys):
        # Move player
        self.player.move(
            keys[pygame.K_a],
            keys[pygame.K_d],
            keys[pygame.K_w],
            keys[pygame.K_s],
            self.game_field
        )

        # Move NPCs
        for npc in self.npcs:
            npc.move(self.game_field)

        # Collision: Player <-> NPC
        for npc in self.npcs:
            dx = npc.x - self.player.x
            dy = npc.y - self.player.y

            if dx * dx + dy * dy <= (player_r + npc_r) ** 2:
                npc.color = "purple"
                npc.hit_timer = 10 # stay purple for 10 frame

        new_npcs = []

        for npc in self.npcs:
            if npc.hit_timer > 0:
                npc.hit_timer -= 1
                if npc.hit_timer == 0:
                    continue  # remove now
            new_npcs.append(npc)

        self.npcs = new_npcs


        if keys[pygame.K_q]:
            self.running = False

    def render_state(self):
        self.graph_engine.start_frame()

        # Draw player
        self.graph_engine.render_circle(
            self.player.x, self.player.y, player_r, "red"
        )

        # Draw NPCs
        for npc in self.npcs:
            self.graph_engine.render_circle(
                npc.x, npc.y, npc_r, npc.color
            )

        self.graph_engine.show_frame()

    def run_game(self):
        clock = pygame.time.Clock()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            keys = pygame.key.get_pressed()
            self.update_state(keys)
            self.render_state()

            clock.tick(self.fps)


# =======================
# Main
# =======================

if __name__ == "__main__":
    game_field = GameField(20, 20, 780, 580)
    player = Player(400, 300)

    npcs = []
    for _ in range(10):
        speed_x = random.choice([-1, 1]) * random.randint(1, 3)
        speed_y = random.choice([-1, 1]) * random.randint(1, 3)

        npc = NPC(
            random.randint(50, 750),
            random.randint(50, 550),
            speed_x,
            speed_y
        )
        npcs.append(npc)

    game_engine = GameEngine(
        GraphicsEngine(),
        game_field,
        player,
        npcs,
        fps=60
    )

    game_engine.run_game()