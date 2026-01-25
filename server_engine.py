from action import PlayerActions

from pygame import Vector2
import time
import random

class ServerGameEngine:
    def __init__(self, game_field, players, npcs, *, fps=60):

        self.game_field = game_field
        self.players = players
        self.npcs = npcs
        self.fps = fps
        self.bullets = []

        self.game_state = {
            "players": {},  # id: {"pos": [x, y], "radius": r}
            "npcs": [],      # [{"pos": Vector2, "vel": Vector2, "radius": r}, ...]
            "bullets": []
        }
    
    def get_game_state_data(self):
        """Returns json for sending to client"""
        # TODO: Everything.
        result = {}
        for p in self.players:
            result[p.id] = (p.x, p.y)

        return result
    
    def update_physics(self):
        for npc in self.game_state["npcs"]:
            npc["pos"] += npc["vel"]

            if npc["pos"].x < 0 or npc["pos"].x > 500:
                npc["vel"].x *= -1
            if npc["pos"].y < 0 or npc["pos"].y > 500:
                npc["vel"].y *= -1

        # check Player vs NPC collision (Removal)
        for p_id in list(self.game_state["players"].keys()):
            p = self.game_state["players"][p_id]
            p_pos = Vector2(p["pos"][0], p["pos"][1])

            # filter out NPCs that hit a player
            self.game_state["npcs"] = [
                n for n in self.game_state["npcs"]
                if (p_pos - n["pos"]).length() > (p["radius"] + n["radius"])
            ]

        # ---move bullet---
        for bullet in self.game_state["bullets"]:
            bullet["pos"] += bullet["vel"]

        # --- Remove bullets outside field ---
        self.game_state["bullets"] = [
            b for b in self.game_state["bullets"]
            if 0 <= b["pos"].x <= 500 and 0 <= b["pos"].y <= 500
        ]

        # --- Bullet vs NPC collision ---
        new_npcs = []

        for npc in self.game_state["npcs"]:
            hit = False
            for bullet in list(self.game_state["bullets"]):  # list() is IMPORTANT
                if (bullet["pos"] - npc["pos"]).length() <= bullet["radius"] + npc["radius"]:
                    hit = True
                    self.game_state["bullets"].remove(bullet)
                    break

            if not hit:
                new_npcs.append(npc)

        self.game_state["npcs"] = new_npcs

        time.sleep(1/60)
    
    def update_player_actions(self, actions: PlayerActions):
        player = self.players[actions.id]
        # update player position
        player.move(actions.move_left, actions.move_right, 
                    actions.move_up, actions.move_down)
        
        # --- Clamp player inside game field ---
        player.pos.x = max(self.game_field.x_min, min(self.game_field.x_max, player.pos.x))
        player.pos.y = max(self.game_field.y_min, min(self.game_field.y_max, player.pos.y))

        player.rotate(actions.move_left, actions.move_right, 
                      actions.move_up, actions.move_down)
        
        # TODO: This is redundant with self.players. game_state should be created by a method instead.
        self.game_state["players"][actions.id] = {
            "pos": player.pos,
            "radius": player.radius
        }

        # spawn 5 NPCs if player clicked
        if actions.spawn_npcs:
            mx, my = actions.spawn_npcs
            for _ in range(5):
                self.game_state["npcs"].append({
                    "pos": Vector2(mx, my),
                    "vel": Vector2(random.uniform(-5, 5), random.uniform(-5, 5)),
                    "radius": 20
                })

        # ---fire bullet---
        if actions.fire:
            # TODO: Use angle of player's orientation instead
            dx, dy = data["fire"]
            self.game_state["bullets"].append({
                "pos": Vector2(data["pos"][0], data["pos"][1]),
                "vel": Vector2(dx, dy).normalize() * 10,
                "radius": 5
            })
