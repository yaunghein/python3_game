class Player:
    def __init__(self, x_pos, y_pos):
        self.x_pos = x_pos
        self.y_pos = y_pos
    
    def move(self, x_delta=0, y_delta=0):
        self.x_pos += x_delta
        self.y_pos += y_delta
    
    def set_pos(self, x, y):
        self.x_pos = x
        self.y_pos = y
    
    def get_pos(self):
        return self.x_pos, self.y_pos

class NPC:
    def __init__(self, x_pos, y_pos, x_speed, y_speed):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.x_speed = x_speed
        self.y_speed = y_speed
    
    def update_pos(self):
        pass