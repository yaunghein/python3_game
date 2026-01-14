# I added minimal properties to these class to start things running
# Maybe we can refactor by moving character codes from GameEngine to here
# Actually, you all can refactor all you want 😁
# And let's discuss

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    

class NPC:
    def __init__(self, name: str, x, y, x_speed, y_speed):
        self.name = name
        self.x = x
        self.y = y
        self.x_speed = x_speed
        self.y_speed = y_speed
    
    def move(self):
        self.x += self.x_speed
        self.y += self.y_speed
