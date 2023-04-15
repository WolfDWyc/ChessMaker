from chessmaker.chess.base import Board
from chessmaker.chess.pieces import King
from chessmaker.chess.results.stalemate import stalemate


def checkmate(board: Board) -> str | None:
    is_stalemate = stalemate(board)
    if is_stalemate:
        current_player = board.current_player
        player_pieces = list(board.get_player_pieces(current_player))

        kings = [piece for piece in player_pieces if isinstance(piece, King)]
        if not kings or all(king.is_attacked() for king in kings):
            return f"Checkmate - {current_player.name} loses"



