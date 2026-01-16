import pygame
import sys
import random
from npc import NPC
from bullet import Bullet


class GameEngine:
    def __init__(self, graph_engine, input_controller, game_field, player, npcs, fps=60):
        self.graph_engine = graph_engine
        self.input_controller = input_controller
        self.game_field = game_field
        self.player = player
        self.npcs = npcs
        self.fps = fps
        self.running = False
        self.game_over = False
        self.bullets = []

    def reset_game(self):
        self.player.reset()
        self.npcs = [
            NPC(random.randint(100, 700), random.randint(100, 500),
                random.randint(-4, 4) or 2, random.randint(-4, 4) or 2,
                npc_type="bad" if i < 1 else "good")
            for i in range(5)
        ]
        self.game_over = False

    def update_state(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.MOUSEBUTTONDOWN and not self.game_over:
                mx, my = pygame.mouse.get_pos()
                for _ in range(5):
                    ntype = "good"
                    # ntype = "bad" if random.random() < 0.3 else "good"
                    self.npcs.append(NPC(mx, my, random.choice(
                        [-4, 4]), random.choice([-4, 4]), npc_type=ntype))

            if event.type == pygame.KEYDOWN and self.game_over:
                if event.key == pygame.K_r:
                    self.reset_game()

        if not self.game_over:
            keys = self.input_controller.get_pressed_keys()
            self.player.move(keys[pygame.K_a], keys[pygame.K_d],
                             keys[pygame.K_w], keys[pygame.K_s], self.game_field)

            p_left, p_right = self.player.x - \
                self.player.radius, self.player.x + self.player.radius
            p_top, p_bottom = self.player.y - \
                self.player.radius, self.player.y + self.player.radius
            for npc in self.npcs[:]:
                npc.move(self.game_field)
                n_left, n_right = npc.x - npc.radius, npc.x + npc.radius
                n_top, n_bottom = npc.y - npc.radius, npc.y + npc.radius
                if p_right > n_left and p_left < n_right and p_bottom > n_top and p_top < n_bottom:
                    if npc.npc_type == "bad":
                        self.game_over = True
                    else:
                        self.npcs.remove(npc)

            if keys[pygame.K_z]:
                self.player.rotate(5)

            if keys[pygame.K_SPACE]:
                # if len(self.bullets) < 10:
                new_bullet = Bullet(
                    self.player.x, self.player.y, self.player.angle)
                self.bullets.append(new_bullet)

            for bullet in self.bullets[:]:
                bullet.move()
                if bullet.is_off_screen(self.graph_engine.width, self.graph_engine.height):
                    self.bullets.remove(bullet)
                    continue

                b_left, b_right = bullet.x - bullet.radius, bullet.x + bullet.radius
                b_top, b_bottom = bullet.y - bullet.radius, bullet.y + bullet.radius
                for npc in self.npcs[:]:
                    n_left, n_right = npc.x - npc.radius, npc.x + npc.radius
                    n_top, n_bottom = npc.y - npc.radius, npc.y + npc.radius
                    if b_right > n_left and b_left < n_right and b_bottom > n_top and b_top < n_bottom:
                        if npc in self.npcs:
                            self.npcs.remove(npc)
                        if bullet in self.bullets:
                            self.bullets.remove(bullet)
                        break

            if keys[pygame.K_q] or keys[pygame.K_ESCAPE]:
                self.running = False

    def render_state(self):
        self.graph_engine.start_frame()
        self.graph_engine.render_circle(
            self.player.x, self.player.y, self.player.radius, "red", self.player.angle)

        for npc in self.npcs:
            if npc.shape == "square":
                self.graph_engine.render_square(
                    npc.x, npc.y, npc.radius, npc.color)
            else:
                self.graph_engine.render_circle(
                    npc.x, npc.y, npc.radius, npc.color)

        for bullet in self.bullets:
            self.graph_engine.render_circle(
                bullet.x, bullet.y, bullet.radius, "red")

        if self.game_over:
            self.graph_engine.render_text("GAME OVER")
            self.graph_engine.render_text(
                "Press 'R' to Restart or 'Q' to Quit", size="small")

        self.graph_engine.show_frame(self.fps)

    def run_game(self):
        self.running = True
        while self.running:
            self.update_state()
            self.render_state()
        pygame.quit()
        sys.exit()
