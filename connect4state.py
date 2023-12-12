import numpy as np

class ConnectFourState:

    def __init__(self, board=None, current_player=1, last_move=None):
        self.board = np.full((6, 7), 0, dtype=np.int8) if board is None else board.copy()
        self.current_player = current_player
        self.last_move = last_move


    def get_valid_moves(self):
        return [col for col in range(7) if self.board[0, col] == 0]


    def copy_and_apply_move(self, col):
        new_state = ConnectFourState(board=self.board, current_player=self.current_player, last_move=col)
        new_state.make_move(col)
        return new_state


    def make_move(self, col):
        row = self.board[:, col]
        row = np.argwhere(row == 0).max()
        self.board[row, col] = self.current_player
        self.current_player = 3 - self.current_player 


    def is_terminal(self):
        return self.check_winner() or np.all(self.board != 0)


    def get_result(self):
        return 1 if (winner := self.check_winner()) == 1 else -1 if winner else 0


    def check_winner(self, inrow=4):
        target = np.array([self.current_player] * inrow)    # Search for 4 inarow of the current player
        rows, cols = self.board.shape

        # Check rows
        for j in range(cols - inrow + 1):
            if any(np.all(target == self.board[:, j:j + inrow], axis=1)):
                return self.current_player

        # Check columns
        for i in range(rows - inrow + 1):
            if any(np.all(target == self.board[i:i + inrow, :].T, axis=1)):
                return self.current_player

        # Check diagonals and anti-diagonals
        for i in range(rows - inrow + 1):
            for j in range(cols - inrow + 1):
                asc_diag = np.diagonal(self.board[i:i + inrow, j:j + inrow])
                des_diag = np.diagonal(np.fliplr(self.board[i:i + inrow, j:j + inrow]))
                if np.all(asc_diag == target) or np.all(des_diag == target):
                    return self.current_player

        return 0