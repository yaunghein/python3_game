import random
from game_engine import GameEngine
from graphic_engine import GraphicsEngine
from player import Player
from npc import NPC
from utils import GameField, InputController


if __name__ == "__main__":
    WIDTH, HEIGHT = 800, 600
    field = GameField(20, 20, WIDTH - 20, HEIGHT - 20)
    hero = Player(WIDTH // 2, HEIGHT // 2, speed=6)

    init_npcs = [
        NPC(random.randint(100, 700), random.randint(100, 500),
            random.randint(-4, 4) or 2, random.randint(-4, 4) or 2,
            npc_type="bad" if i < 1 else "good")
        for i in range(5)
    ]

    graphics = GraphicsEngine(WIDTH, HEIGHT)
    inputs = InputController()
    engine = GameEngine(graphics, inputs, field, hero, init_npcs, fps=60)
    engine.run_game()
