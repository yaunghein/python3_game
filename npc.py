class NPC:
    def __init__(self, x, y, speed_x=3, speed_y=3, radius=20, npc_type="good"):
        self.x = x
        self.y = y
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.radius = radius
        self.npc_type = npc_type  # "good" or "bad"

        if self.npc_type == "bad":
            self.shape = "square"
            self.color = "purple"
        else:
            self.shape = "circle"
            self.color = "blue"

    def move(self, game_field):
        self.x += self.speed_x
        self.y += self.speed_y

        self.x, self.y, x_edge, y_edge = game_field.clamp(self.x, self.y)
        if x_edge:
            self.speed_x *= -1
        if y_edge:
            self.speed_y *= -1
