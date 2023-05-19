from chessmaker.chess.base import Board
from chessmaker.chess.pieces import King


def no_kings(board: Board) -> str | None:
    for player in board.players:
        if not [piece for piece in board.get_player_pieces(player) if isinstance(piece, King)]:
            return f"No kings left - {player.name} loses"
