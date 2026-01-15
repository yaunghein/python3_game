import time
from kb_poller import KBPoller
from characters import Player, NPC


class GameEngine:
    def __init__(self, graphics_engine):
        self.kb = KBPoller()
        self.graphics = graphics_engine
        self.running = True

        self.player = Player(10, 10, 'Circle', 'circle')
        self.npc = NPC(50, 50, 'Square', 'square', 1, 1)
        self.x_max, self.y_max = 100, 100

    def run(self):
        while self.running:
            pressed_keys = self.kb.pressed
            self.handle_input(pressed_keys)
            self.update_physics()
            # self.graphics.render(self.player, self.npc)
            self.graphics.render_state([self.player, self.npc])
            time.sleep(0.5)

    def handle_input(self, keys):
        if "q" in keys:
            self.running = False
        if "a" in keys:
            self.player.x -= 1
        if "d" in keys:
            self.player.x += 1
        if "w" in keys:
            self.player.y -= 1
        if "s" in keys:
            self.player.y += 1

    def update_physics(self):
        if self.npc.x >= self.x_max or self.npc.x <= 0:
            self.npc.x_dir *= -1
        self.npc.x += 5 * self.npc.x_dir

        if self.npc.y >= self.y_max or self.npc.y <= 0:
            self.npc.y_dir *= -1
        self.npc.y += 10 * self.npc.y_dir
