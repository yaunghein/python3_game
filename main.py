from utils import GameField
from game_engine import GameEngine
from graphics import GraphicsEngine
from characters import Player

if __name__ == "__main__":
    game_field = GameField(0, 0, 500, 500)
    player = Player(250, 250, speed_x=7, speed_y=7, radius=20)
    player.angle = 0

    game_engine = GameEngine(
        GraphicsEngine(),
        game_field,
        player,
        [],
        fps=60
    )
    game_engine.run_game()
