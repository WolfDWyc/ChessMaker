from chessmaker.chess.base.board import Board
from chessmaker.chess.results.checkmate import checkmate
from chessmaker.chess.results.no_captures_or_pawn_moves import NoCapturesOrPawnMoves
from chessmaker.chess.results.repetition import Repetition
from chessmaker.chess.results.stalemate import stalemate


def standard_result(board: Board):
    for result in [checkmate, stalemate, Repetition(), NoCapturesOrPawnMoves()]:
        result = result(board)
        if result:
            return result
