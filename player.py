class Player:
    def __init__(self, x, y, speed=5, radius=20):
        self.start_pos = (x, y)
        self.x = x
        self.y = y
        self.speed = speed
        self.radius = radius
        self.angle = 0

    def reset(self):
        self.x, self.y = self.start_pos
        self.angle = 0

    def move(self, left, right, up, down, game_field):
        if left:
            self.x -= self.speed
        if right:
            self.x += self.speed
        if up:
            self.y -= self.speed
        if down:
            self.y += self.speed
        self.x, self.y, _, _ = game_field.clamp(self.x, self.y)

    def rotate(self, amount):
        self.angle = (self.angle + amount) % 360
