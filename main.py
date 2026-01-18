from utils import GameField
from game_engine import GameEngine
from graphics import GraphicsEngine
from characters import Player, NPC


if __name__ == "__main__":
    game_field = GameField(0, 0, 1280, 720)
    player = Player(640, 360, speed_x=5, speed_y=5, radius=20)
    npcs = [NPC(200, 200, 5, 5, radius=20)]

    game_engine = GameEngine(
        GraphicsEngine(),
        # InputController(),
        game_field,
        player,
        npcs,
        fps=15
    )
    game_engine.run_game()
