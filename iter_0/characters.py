# I added minimal properties to these class to start things running
# Maybe we can refactor by moving character codes from GameEngine to here
# Actually, you all can refactor all you want 😁
# And let's discuss

class Player:
    def __init__(self, x, y, name, shape):
        self.name = name
        self.shape = shape
        self.x = x
        self.y = y


class NPC(Player):
    def __init__(self, x, y, name, shape, x_speed, y_speed):
        super().__init__(x, y, name, shape)
        self.x_speed = x_speed
        self.y_speed = y_speed

    def move(self):
        self.x += self.x_speed
        self.y += self.y_speed
