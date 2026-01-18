import socket
import pickle
import threading
import time
import random
from pygame import Vector2

SERVER = "127.0.0.1"
PORT = 5555

# Global Game State
game_state = {
    "players": {},  # id: {"pos": [x, y], "radius": r}
    "npcs": []      # [{"pos": Vector2, "vel": Vector2, "radius": r}, ...]
}


def update_physics():
    while True:
        for npc in game_state["npcs"]:
            npc["pos"] += npc["vel"]

            if npc["pos"].x < 0 or npc["pos"].x > 500:
                npc["vel"].x *= -1
            if npc["pos"].y < 0 or npc["pos"].y > 500:
                npc["vel"].y *= -1

        # check Player vs NPC collision (Removal)
        for p_id in list(game_state["players"].keys()):
            p = game_state["players"][p_id]
            p_pos = Vector2(p["pos"][0], p["pos"][1])

            # filter out NPCs that hit a player
            game_state["npcs"] = [
                n for n in game_state["npcs"]
                if (p_pos - n["pos"]).length() > (p["radius"] + n["radius"])
            ]

        time.sleep(1/60)


def handle_client(conn, player_id):
    conn.send(pickle.dumps(player_id))
    while True:
        try:
            # Receive: {"pos": [x,y], "radius": r, "spawn": [mx, my] or None}
            data = pickle.loads(conn.recv(4096))
            if not data:
                break

            # update player position
            game_state["players"][player_id] = {
                "pos": data["pos"], "radius": data["radius"]}

            # spawn 5 NPCs if player clicked
            if data["spawn"]:
                mx, my = data["spawn"]
                for _ in range(5):
                    game_state["npcs"].append({
                        "pos": Vector2(mx, my),
                        "vel": Vector2(random.uniform(-5, 5), random.uniform(-5, 5)),
                        "radius": 20
                    })

            conn.sendall(pickle.dumps(game_state))
        except:
            break

    if player_id in game_state["players"]:
        del game_state["players"][player_id]
    conn.close()


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((SERVER, PORT))
s.listen()
threading.Thread(target=update_physics, daemon=True).start()

print("Server started. Waiting for connections...")
player_count = 0
while True:
    conn, addr = s.accept()
    threading.Thread(target=handle_client, args=(conn, player_count)).start()
    player_count += 1
