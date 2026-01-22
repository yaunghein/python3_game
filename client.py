from graphics import GraphicsEngine
from utils import GameField
from action import PlayerActions

import socket
import pygame

HOST = '127.0.0.1'
PORT = 21001

running = True


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print("Connected to server")

    engine = GraphicsEngine()  # pygame.init() is inside

    while running:
        actions = PlayerActions()
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
        state = eval(state_data.decode())

        # {1: (97, 3), 'self': 1}
        print("State received:", state)

        engine.start_frame()

        for player_id, positions in state.items():
            if player_id == "self":
                continue
            engine.render_circle(positions[0], positions[1], 20, "green" if player_id == state["self"] else "blue")

        engine.show_frame()