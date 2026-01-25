import json

class PlayerActions:
    def __init__(self, player_id, action_json=None):
        self.id = player_id
        if action_json:
            action_dict = json.loads(action_json)
            self.move_left = action_dict["move_left"]
            self.move_right = action_dict["move_right"]
            self.move_up = action_dict["move_up"]
            self.move_down = action_dict["move_down"]
            self.rotate = action_dict["rotate"]
            self.fire = action_dict["fire"]
            self.spawn_npcs = action_dict["spawn_npcs"]
        else:
            self.move_left = False
            self.move_right = False
            self.move_up = False
            self.move_down = False
            self.rotate = None
            self.fire = False
            self.spawn_npcs = None
    
    def to_json(self):
        """Return json string"""
        return ""
    
