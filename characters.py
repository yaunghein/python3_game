from pygame import Vector2
import math


class Character:
    def __init__(self, x, y, speed_x=1, speed_y=1, radius=8):
        self.pos = Vector2(x, y)
        self.vel = Vector2(speed_x, speed_y)
        self.radius = radius
        self.mass = math.pi * (self.radius ** 2)


class Player(Character):
    def __init__(self, x, y, speed_x=1, speed_y=1, radius=8, angle=0):
        super().__init__(x, y, speed_x, speed_y, radius)
        self.mass = 0  # the player is immovable except via keyboard input
        self.angle = 0

    def move(self, left, right, up, down):
        self.pos.x += self.vel.x * right - self.vel.x * left
        self.pos.y += self.vel.y * down - self.vel.y * up

    # TODO: Change this to accept scroll wheel instead
    def rotate(self, left, right, up, down):
        if right:
            if up:
                self.angle = 45
            elif down:
                self.angle = 315
        elif left:
            if up:
                self.angle = 135
            elif down:
                self.angle = 225



class NPC(Character):
    def __init__(self, x, y, speed_x=1, speed_y=1, radius=8):
        super().__init__(x, y, speed_x, speed_y, radius)

    def move(self):
        self.pos += self.vel


class Bullet:
    def __init__(self, pos, direction, speed=10):
        self.pos = Vector2(pos.x, pos.y)
        self.vel = direction.normalize() * speed
        self.radius = 4

    def move(self):
        self.pos += self.vel