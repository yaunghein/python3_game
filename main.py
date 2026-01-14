from engines.game import GameEngine
from engines.graphics import GraphicsEngine


def main():
    graphics = GraphicsEngine()
    game = GameEngine(graphics)

    print("Game Started. Press 'q' to quit.")
    game.run()


if __name__ == "__main__":
    main()
