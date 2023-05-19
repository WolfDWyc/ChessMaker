from chessmaker.chess.base import Board
from chessmaker.chess.pieces import King
from chessmaker.chess.results.stalemate import stalemate


def checkmate(board: Board) -> str | None:
    current_player = board.current_player
    kings = [piece for piece in board.get_player_pieces(current_player) if isinstance(piece, King)]

    if stalemate(board) and all(king.is_attacked() for king in kings):
        return f"Checkmate - {current_player.name} loses"
