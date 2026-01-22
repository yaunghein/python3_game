import json

class PlayerActions:
    def __init__(self, action_json=None):
        if action_json:
            action_dict = json.loads(action_json)
            self.move_left = action_dict["move_left"]
            self.move_right = action_dict["move_right"]
            self.move_up = action_dict["move_up"]
            self.move_down = action_dict["move_down"]
            self.rotate = action_dict["rotate"]
            self.shoot = action_dict["shoot"]
            self.spawn_npcs = action_dict["spawn_npcs"]
        else:
            self.move_left = False
            self.move_right = False
            self.move_up = False
            self.move_down = False
            self.rotate = None
            self.shoot = False
            self.spawn_npcs = None
    
    def to_json(self):
        """Return json string"""
        return ""
    
