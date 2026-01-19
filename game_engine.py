import pygame
from characters import Bullet
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
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        direction = self.player.vel
                        if direction.length() == 0:
                            direction = Vector2(1, 0)  # default direction
                        
                        fire_direction = [direction.x, direction.y]

            keys = pygame.key.get_pressed()
            self.player.move(keys[pygame.K_a], keys[pygame.K_d],
                             keys[pygame.K_w], keys[pygame.K_s])
            
            # ---update orientation---
            direction = Vector2(0, 0)

            if keys[pygame.K_a]:
                direction.x = -1
            if keys[pygame.K_d]:
                direction.x = 1
            if keys[pygame.K_w]:
                direction.y = -1
            if keys[pygame.K_s]:
                direction.y = 1

            if direction.length() > 0:
                direction = direction.normalize()
                self.player.vel = direction

                speed = 7
                self.player.pos += direction * speed

            # --- Clamp player inside game field ---
            self.player.pos.x = max(self.game_field.x_min, min(self.game_field.x_max, self.player.pos.x))
            self.player.pos.y = max(self.game_field.y_min, min(self.game_field.y_max, self.player.pos.y))

            # send local data, get global state
            payload = {
                "pos": [self.player.pos.x, self.player.pos.y],
                "radius": self.player.radius,
                "spawn": click_to_send,
                "fire": fire_direction }
            world_state = self.net.send(payload)
            click_to_send = None  # reset after sending

            if world_state:
                self.graph_engine.start_frame()

                # draw all players
                for p_id, p_data in world_state["players"].items():
                    color = "red" if p_id == self.net.p_id else "white"
                    self.graph_engine.render_circle(
                        Vector2(p_data["pos"][0], p_data["pos"][1]), p_data["radius"], color)
                    
                # --- draw player orientation ---
                start = Vector2(p_data["pos"][0], p_data["pos"][1])
                direction = self.player.vel

                if direction.length() > 0:
                    end = start + direction.normalize() * 30
                    pygame.draw.line(
                        self.graph_engine.screen,
                        "yellow",
                        start,
                        end,
                        3
                    )

                # draw all NPCs
                for npc in world_state["npcs"]:
                    self.graph_engine.render_circle(
                        npc["pos"], npc["radius"], "blue")

                # --- Draw bullets ---
                for bullet in world_state["bullets"]:
                    self.graph_engine.render_circle(
                        bullet["pos"],
                        bullet["radius"],
                        "yellow"
                    )

                self.graph_engine.show_frame()

            self.clock.tick(self.fps)