from kb_poller import KBPoller

from utils import GameField, InputController
from game_engine import GameEngine
from graphics import GraphicsEngine
from characters import Player, NPC


if __name__ == "__main__":
    game_field = GameField(0, 0, 100, 100)
    player = Player(50, 50)
    npc = NPC(70, 70, 2, 1)

    game_engine = GameEngine(GraphicsEngine(), InputController(
        KBPoller()), game_field, player, npc, fps=15)
    game_engine.run_game()
