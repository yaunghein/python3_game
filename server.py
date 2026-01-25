import socket
import pickle
import threading
import time
import random
from pygame import Vector2

SERVER = "127.0.0.1"
PORT = 5555

game_state = {
    "players": {},
    "npcs": [],
    "bullets": []
}


def update_physics():
    while True:
        for npc in game_state["npcs"]:
            npc["pos"] += npc["vel"]
            if npc["pos"].x < 0 or npc["pos"].x > 500:
                npc["vel"].x *= -1
            if npc["pos"].y < 0 or npc["pos"].y > 500:
                npc["vel"].y *= -1

        for p_id in list(game_state["players"].keys()):
            p = game_state["players"][p_id]
            p_pos = Vector2(p["pos"][0], p["pos"][1])
            game_state["npcs"] = [
                n for n in game_state["npcs"]
                if (p_pos - n["pos"]).length() > (p["radius"] + n["radius"])
            ]

        for bullet in game_state["bullets"]:
            bullet["pos"] += bullet["vel"]

        game_state["bullets"] = [
            b for b in game_state["bullets"]
            if 0 <= b["pos"].x <= 500 and 0 <= b["pos"].y <= 500
        ]

        new_npcs = []
        for npc in game_state["npcs"]:
            hit = False
            for bullet in list(game_state["bullets"]):
                if (bullet["pos"] - npc["pos"]).length() <= bullet["radius"] + npc["radius"]:
                    hit = True
                    game_state["bullets"].remove(bullet)
                    break
            if not hit:
                new_npcs.append(npc)
        game_state["npcs"] = new_npcs

        time.sleep(1/60)


def handle_client(conn, player_id):
    conn.send(pickle.dumps(player_id))
    while True:
        try:
            data = pickle.loads(conn.recv(4096))
            if not data:
                break

            game_state["players"][player_id] = {
                "pos": data["pos"],
                "radius": data["radius"],
                "angle": data.get("angle", 0)
            }

            if data["spawn"]:
                mx, my = data["spawn"]
                for _ in range(5):
                    game_state["npcs"].append({
                        "pos": Vector2(mx, my),
                        "vel": Vector2(random.uniform(-5, 5), random.uniform(-5, 5)),
                        "radius": 20
                    })

            if data["fire"]:
                dx, dy = data["fire"]
                game_state["bullets"].append({
                    "pos": Vector2(data["pos"][0], data["pos"][1]),
                    "vel": Vector2(dx, dy) * 10,
                    "radius": 5
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

player_count = 0
while True:
    conn, addr = s.accept()
    threading.Thread(target=handle_client, args=(conn, player_count)).start()
    player_count += 1
