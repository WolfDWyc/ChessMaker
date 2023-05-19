from collections import defaultdict

from chessmaker.chess.base import Board, Position


class Repetition:
    def __init__(self, needed_repetitions: int = 3):
        self.needed_repetitions = needed_repetitions
        self.positions = defaultdict(int)

    def __call__(self, board: Board) -> str | None:
        position_hash = ""
        for y in range(board.size[1]):
            for x in range(board.size[0]):
                square = board[Position(x, y)]
                if square is None:
                    position_hash += "None"
                elif square.piece is None:
                    position_hash += "Empty"
                else:
                    position_hash += square.piece.__class__.__name__ + square.piece.player._id

        self.positions[position_hash] = self.positions.get(position_hash, 0) + 1
        if self.positions[position_hash] >= self.needed_repetitions:
            return "Repetition - Draw"
