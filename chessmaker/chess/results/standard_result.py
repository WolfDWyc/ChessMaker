from chessmaker.chess.base.board import Board
from chessmaker.chess.results import no_kings
from chessmaker.chess.results.checkmate import checkmate
from chessmaker.chess.results.no_captures_or_pawn_moves import NoCapturesOrPawnMoves
from chessmaker.chess.results.repetition import Repetition
from chessmaker.chess.results.stalemate import stalemate


class StandardResult:
    def __init__(self):
        self.results = [
            no_kings,
            checkmate,
            stalemate,
            Repetition(),
            NoCapturesOrPawnMoves(),
        ]

    def __call__(self, board: Board):
        for result in self.results:
            result = result(board)
            if result:
                return result
