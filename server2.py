



if __name__ == "__main__":
    game_field = GameField(0, 0, 600, 600)
    # player = Player(1, 50, 50, speed_x=3, speed_y=3)
    npcs = [NPC(70, 70, 2, 1)]

    game_engine = ServerGameEngine(
        game_field,
        [],
        npcs,
        fps=60)

    players_data_exchange_thread = Thread(target=conection_listener_thread_function, args=(game_engine,))
    players_data_exchange_thread.start()

    game_engine.run_game()