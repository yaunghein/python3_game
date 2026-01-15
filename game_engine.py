import time
import pygame


class GameEngine:
    def __init__(self, graph_engine, game_field, player, npcs, *, fps=60):

        self.graph_engine = graph_engine

        self.game_field = game_field
        self.player = player
        self.npcs = npcs
        self.fps = fps

    def update_state(self, keys):
        self.npc.move(self.game_field)
        self.player.move(keys[pygame.K_a], keys[pygame.K_d],
                         keys[pygame.K_w], keys[pygame.K_s], self.game_field)
        
        for i in len(self.npcs):
            npc = self.npcs[i]

        

        if keys[pygame.K_q]:
            self.running = False
    
    def handle_collision():
        pass

    def render_state(self):
        self.graph_engine.start_frame()

        self.graph_engine.render_circle(
            self.player.x, self.player.y, self.player.radius, "red")
        
        for npc in self.npcs:
            self.graph_engine.render_circle(self.npc.x, self.npc.y, self.npc.radius, "blue")

        self.graph_engine.show_frame()

    # def subscribe_events(self):

    def run_game(self):
        self.running = True

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            keys = pygame.key.get_pressed()
            self.update_state(keys)
            self.render_state()
            pygame.display.flip()

            time.sleep(1 / self.fps)
