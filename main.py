from utils import GameField
from game_engine import GameEngine
from graphics import GraphicsEngine
from characters import Player

if __name__ == "__main__":
    game_field = GameField(0, 0, 500, 500)
    # Each client creates their local player object
    player = Player(250, 250, speed_x=7, speed_y=7, radius=20)

    game_engine = GameEngine(
        GraphicsEngine(),
        game_field,
        player,
        [],  # NPCs list is now managed by server
        fps=60
    )
    game_engine.run_game()
