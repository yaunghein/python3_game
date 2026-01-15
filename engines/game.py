import time
from kb_poller import KBPoller
from characters import Player, NPC


class GameEngine:
    def __init__(self, graphics_engine):
        self.kb = KBPoller()
        self.graphics = graphics_engine
        self.running = True

        self.player = Player(10, 10, 'Circle', 'circle')
        self.npc = NPC(50, 50, 'Square', 'square', 5, 10)
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
        # for npc in self.npc:
        self.npc.move()
        self.validate_bound_bouncing(self.npc)

        self.validate_bound_sticking(self.player)

    def validate_bound_bouncing(self, npc: NPC):
        if npc.x > self.x_max:
            npc.x_speed = - npc.x_speed
            npc.x = self.x_max - (npc.x - self.x_max)
        elif npc.x < 0:
            npc.x_speed = - npc.x_speed
            npc.x = - npc.x

        if npc.y > self.y_max:
            npc.y_speed = - npc.y_speed
            npc.y = self.y_max - (npc.y - self.y_max)
        elif npc.y < 0:
            npc.y_speed = - npc.x_speed
            npc.y = - npc.y

    def validate_bound_sticking(self, player: Player):
        if player.x < 0:
            player_x = 0
        if player.x > self.x_max:
            player_x = self.x_max

        if player.y < 0:
            player_y = 0
        if player.y > self.y_max:
            player_y = self.y_max
