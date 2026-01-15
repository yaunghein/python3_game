from pygame import Vector2
import math

class Character:
    def __init__(self, x, y, speed_x=1, speed_y=1, radius=8):
        self.pos = Vector2(x, y)
        self.vel = Vector2(speed_x, speed_y)
        self.radius = radius
        self.mass = math.pi * (self.radius ** 2)


class Player(Character):
    def __init__(self, x, y, speed_x=1, speed_y=1, radius=8):
        super().__init__(x, y, speed_x, speed_y, radius)

    def move(self, left, right, up, down, game_field):
        self.pos.x += self.vel.x * right - self.vel.x * left
        self.pos.y += self.vel.y * down - self.vel.y * up

        # TODO: Change GameField
        self.pos, _, _ = game_field.clamp(self.pos)


class NPC(Character):
    def __init__(self, x, y, speed_x=1, speed_y=1, radius=8):
        super().__init__(x, y, speed_x, speed_y, radius)

    def move(self, game_field):
        self.pos += self.vel

        # Move this to game engine
        self.pos, x_edge, y_edge = game_field.clamp(self.pos)

        if x_edge:
            self.vel.x = -self.vel.x

        if y_edge:
            self.vel.y = -self.vel.y