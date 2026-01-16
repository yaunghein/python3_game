import math


class Bullet:
    def __init__(self, x, y, angle, speed=10, radius=3):
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = speed
        self.rad = math.radians(angle)

    def move(self):
        self.x += math.cos(self.rad) * self.speed + 1
        self.y += math.sin(self.rad) * self.speed

    def is_off_screen(self, width, height):
        return self.x < 0 or self.x > width or self.y < 0 or self.y > height
