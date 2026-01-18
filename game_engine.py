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

    def run_game(self):
        self.running = True
        click_to_send = None

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    click_to_send = pygame.mouse.get_pos()

            keys = pygame.key.get_pressed()
            self.player.move(keys[pygame.K_a], keys[pygame.K_d],
                             keys[pygame.K_w], keys[pygame.K_s])

            # send local data, get global state
            payload = {
                "pos": [self.player.pos.x, self.player.pos.y],
                "radius": self.player.radius,
                "spawn": click_to_send
            }
            world_state = self.net.send(payload)
            click_to_send = None  # reset after sending

            if world_state:
                self.graph_engine.start_frame()

                # draw all players
                for p_id, p_data in world_state["players"].items():
                    color = "red" if p_id == self.net.p_id else "white"
                    self.graph_engine.render_circle(
                        Vector2(p_data["pos"][0], p_data["pos"][1]), p_data["radius"], color)

                # draw all NPCs
                for npc in world_state["npcs"]:
                    self.graph_engine.render_circle(
                        npc["pos"], npc["radius"], "blue")

                self.graph_engine.show_frame()

            self.clock.tick(self.fps)
