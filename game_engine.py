import pygame
from network import Network
from pygame import Vector2


class GameEngine:
    def __init__(self, graph_engine, game_field, player, npcs, *, fps=60):
        self.graph_engine = graph_engine
        self.player = player
        self.fps = fps
        self.clock = pygame.time.Clock()
        self.net = Network()
        self.game_field = game_field
        self.bullets = []

    def run_game(self):
        self.running = True
        click_to_send = None

        while self.running:
            fire_direction = None

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    click_to_send = pygame.mouse.get_pos()

            keys = pygame.key.get_pressed()

            move_dir = Vector2(0, 0)
            if keys[pygame.K_a]:
                move_dir.x = -1
            if keys[pygame.K_d]:
                move_dir.x = 1
            if keys[pygame.K_w]:
                move_dir.y = -1
            if keys[pygame.K_s]:
                move_dir.y = 1

            if move_dir.length() > 0:
                move_dir = move_dir.normalize()
                self.player.pos += move_dir * 7

            if keys[pygame.K_z]:
                self.player.angle = (self.player.angle + 5) % 360

            if keys[pygame.K_SPACE]:
                bullet_vec = Vector2(1, 0).rotate(self.player.angle)
                fire_direction = [bullet_vec.x, bullet_vec.y]

            self.player.pos.x = max(self.game_field.x_min, min(
                self.game_field.x_max, self.player.pos.x))
            self.player.pos.y = max(self.game_field.y_min, min(
                self.game_field.y_max, self.player.pos.y))

            payload = {
                "pos": [self.player.pos.x, self.player.pos.y],
                "angle": self.player.angle,
                "radius": self.player.radius,
                "spawn": click_to_send,
                "fire": fire_direction
            }
            world_state = self.net.send(payload)
            click_to_send = None

            if world_state:
                self.graph_engine.start_frame()

                for p_id, p_data in world_state["players"].items():
                    color = "red" if p_id == self.net.p_id else "white"
                    p_pos = Vector2(p_data["pos"][0], p_data["pos"][1])
                    self.graph_engine.render_circle(
                        p_pos, p_data["radius"], color)

                    p_angle = p_data.get("angle", 0)
                    look_vec = Vector2(1, 0).rotate(p_angle) * 30
                    pygame.draw.line(self.graph_engine.screen,
                                     "yellow", p_pos, p_pos + look_vec, 3)

                for npc in world_state["npcs"]:
                    self.graph_engine.render_circle(
                        npc["pos"], npc["radius"], "blue")

                for bullet in world_state["bullets"]:
                    self.graph_engine.render_circle(
                        bullet["pos"], bullet["radius"], "yellow")

                self.graph_engine.show_frame()

            self.clock.tick(self.fps)
