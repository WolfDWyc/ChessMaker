from chessmaker.chess.base import Board
from chessmaker.chess.pieces import King


def double_check_to_win(board: Board) -> str | None:
    current_player = board.current_player
    player_pieces = list(board.get_player_pieces(current_player))

    kings = [piece for piece in player_pieces if isinstance(piece, King)]
    for king in kings:
        attacker_count = 0
        position = king.position
        for piece in board.get_pieces():
            if piece.player != current_player:
                for move_option in piece.get_move_options():
                    if position in move_option.captures:
                        attacker_count += 1
                        break

        if attacker_count >= 2:
            return f"Double check - {current_player.name} loses"
