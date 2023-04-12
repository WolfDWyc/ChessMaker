from typing import Callable

from src.chess.base.board import Board, AfterNewPieceEvent
from src.chess.base.piece import Piece


def for_all_pieces(board: Board, func: Callable[[Piece], None], piece_type: type = Piece, player = None) -> None:
    get_pieces = board.get_pieces
    if player is not None:
        get_pieces = lambda: board.get_player_pieces(player)
    for _piece in get_pieces():
        if isinstance(_piece, piece_type):
            func(_piece)

    def on_new_piece(event: AfterNewPieceEvent):
        if isinstance(event.piece, piece_type) and (player is None or event.piece.player == player):
            func(event.piece)

    board.subscribe(AfterNewPieceEvent, on_new_piece)