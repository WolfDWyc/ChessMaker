from chessmaker.chess.base import Board


def stalemate(board: Board) -> str | None:
    current_player = board.current_player
    player_pieces = list(board.get_player_pieces(current_player))
    for piece in player_pieces:
        if piece.get_move_options():
            return None

    return "Stalemate - Draw"