from graphics import GraphicsEngine
from utils import GameField
from action import PlayerActions

import socket
import pygame
from pygame import Vector2
import pickle

HOST = '127.0.0.1'
PORT = 21001

running = True
fps = 30


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    this_player_id = pickle.loads(s.recv(2048))
    print("Connected to server")

    engine = GraphicsEngine()  # pygame.init() is inside
    clock = pygame.time.Clock()

    while running:
        actions = PlayerActions(this_player_id)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                actions.spawn_npcs = list(pygame.mouse.get_pos())
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    actions.shoot = True

        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:
            running = False
        if keys[pygame.K_a]:
            actions.move_left = True
        if keys[pygame.K_d]:
            actions.move_right = True
        if keys[pygame.K_w]:
            actions.move_up = True
        if keys[pygame.K_s]:
            actions.move_down = True

        s.send(actions.to_json().encode())

        print("Waiting for state...")
        state_data = s.recv(1024)
        world_state = eval(state_data.decode())

        # {1: (97, 3), 'self': 1}
        print("State received:", world_state)

        if world_state:
            engine.start_frame()

            # draw all players
            for p_id, p_data in world_state["players"].items():
                color = "red" if p_id == this_player_id else "white"
                engine.render_circle(
                    Vector2(p_data["pos"][0], p_data["pos"][1]), p_data["radius"], color)
                
                # --- draw player orientation ---
                start = Vector2(p_data["pos"][0], p_data["pos"][1])
                direction = p_data["vel"]  ## TODO: add this elsewhere

                if direction.length() > 0:
                    end = start + direction.normalize() * 30
                    pygame.draw.line(
                        engine.screen,
                        "yellow",
                        start,
                        end,
                        3
                    )

            # draw all NPCs
            for npc in world_state["npcs"]:
                engine.render_circle(
                    npc["pos"], npc["radius"], "blue")

            # --- Draw bullets ---
            for bullet in world_state["bullets"]:
                engine.render_circle(
                    bullet["pos"],
                    bullet["radius"],
                    "yellow"
                )

            engine.show_frame()

        clock.tick(fps)
        engine.start_frame()
        engine.show_frame()