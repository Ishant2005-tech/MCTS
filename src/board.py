from config.config import *
from utils.utils import indices_from_move
import numpy as np

class TTTBoard:
    def __init__(self, display_type = "console"):
        """
        Initialize the Tic Tac Toe board.

        Parameters
        ----------
        display_type : str, default = "console"
            The type of display to use. Options are "console" and "gui".
        """
        # TODO: create a gui for the board

        self.board = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.board = np.array(self.board)   
        self.display_type = display_type
        if self.display_type == "console":
            self.symbol_map = SYMBOL_CHARS
        self.outcome = None
        self.player = X

    @property
    def winner(self):
        return SYMBOL_CHARS[self.outcome]

    @property
    def available_moves(self):
        if self.is_game_over():
            return []
        return [move + 1 for move in range(BOARD_SIZE ** 2) if self.board[move // BOARD_SIZE][move % BOARD_SIZE] == EMPTY]
    
    def play_turn(self, move):
        """
        Executes a player's move on the board and switches to the next player.

        Parameters
        ----------
        move : int 
            The move to be played by the current player. This is a row major based index
            representing the position on the board where the player wants to mark.
            Valid values are 1 to BOARD_SIZE ** 2.

        """
        if move not in self.available_moves:
            print(f"Invalid move: {move}, Available moves: {self.available_moves}")
            return False
        row, col = indices_from_move(move)
        self.board[row][col] = self.player
        self.player = -self.player
        return True

    def display(self):
        for row in self.board:
            if self.display_type == "console":
                print(" ".join([self.symbol_map[symbol] for symbol in row]))
            else:
                print(" ".join(row))

    def evaluate_outcome(self):
        # EVALUATE ROWS
        if np.any(self.board.sum(axis=1) == BOARD_SIZE):
            self.outcome = X
        elif np.any(self.board.sum(axis=1) == -BOARD_SIZE):
            self.outcome = O
        # EVALUATE COLUMNS
        elif np.any(self.board.sum(axis=0) == BOARD_SIZE):
            self.outcome = X
        elif np.any(self.board.sum(axis=0) == -BOARD_SIZE):
            self.outcome = O
        # EVALUATE DIAGONALS
        elif np.trace(self.board) == BOARD_SIZE:
            self.outcome = X
        elif np.trace(self.board) == -BOARD_SIZE:
            self.outcome = O
        elif np.trace(np.fliplr(self.board)) == BOARD_SIZE:
            self.outcome = X
        elif np.trace(np.fliplr(self.board)) == -BOARD_SIZE:
            self.outcome = O
        # NO WINNER
        elif np.all(self.board != EMPTY):
            self.outcome = EMPTY

        return self.outcome

    def is_game_over(self):
        if self.evaluate_outcome() is not None:
            return True
        return False
    
    def reset(self):    
        self.board = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.board = np.array(self.board)
        self.player = X
        self.outcome = None
        
        
if __name__ == "__main__":
    board = TTTBoard()
    board.board[0][0] = X
    board.board[1][1] = X
    board.board[2][2] = X
    # board.board[3][3] = X
    print(board.evaluate_outcome())
    print(board.is_game_over())
    print(board.available_moves)
    board.display()