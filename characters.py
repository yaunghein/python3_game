# I added minimal properties to these class to start things running
# Maybe we can refactor by moving character codes from GameEngine to here
# Actually, you all can refactor all you want 😁
# And let's discuss

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class NPC:
    def __init__(self, x, y, x_dir, y_dir):
        self.x = x
        self.y = y
        self.x_dir = x_dir
        self.y_dir = y_dir
