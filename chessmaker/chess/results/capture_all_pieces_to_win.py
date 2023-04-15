from chessmaker.chess.base import Board


def capture_all_pieces_to_win(board: Board) -> str | None:
    lost_players = []
    for player in board.players:
        if len(list(board.get_player_pieces(player))) == 0:
            lost_players.append(player)

    if len(lost_players) == 0:
        return None

    if len(lost_players) == 1:
        return f"All pieces captured - {lost_players[0].name} loses"

    return "Multiple players have no pieces - Draw"
