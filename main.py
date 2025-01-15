from src.board import TTTBoard
from src.agent import MCTSagent, RandomAgent
from config.config import *
import numpy as np

rng = np.random.default_rng(RNG_SEED)

if __name__ == "__main__":
    board = TTTBoard()
    agent = MCTSagent()
    # agent = RandomAgent()

    board.display()
    while True:
        print("Available moves: ", board.available_moves)
        input_move = int(input("Enter your move: "))
        success = board.play_turn(input_move)
        if not success:
            board.display()
            continue
        move = agent.get_move(board)
        if move is not None:
            board.play_turn(move)
        board.display()
        print('\n'+"#"*10+'\n')
        if board.is_game_over():
            print(f"{board.winner} wins")
            break
