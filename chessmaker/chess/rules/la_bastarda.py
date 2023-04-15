from typing import Callable

from chessmaker.chess.base import Board, as_rule, Position, BeforeGetMoveOptionsEvent, AfterNewPieceEvent, \
    AfterMoveEvent, Piece, Rule, Player
from chessmaker.chess.piece_utils import is_in_board
from chessmaker.chess.pieces import King, Queen, Pawn
from chessmaker.events import EventPriority


class LaBastarda(Rule):
    def __init__(self, pawn: Callable[[Player], Pawn]):
        self._pawn = pawn

    def on_join_board(self, board: Board):
        for piece in board.get_pieces():
            self.subscribe_to_piece(piece)
        board.subscribe(AfterNewPieceEvent, self.on_after_new_piece)

    def on_after_new_piece(self, event: AfterNewPieceEvent):
        self.subscribe_to_piece(event.piece)

    def subscribe_to_piece(self, piece: Piece):
        if isinstance(piece, King):
            piece.subscribe(BeforeGetMoveOptionsEvent, self.on_before_get_move_options, EventPriority.HIGH)
            piece.subscribe(AfterMoveEvent, self.on_after_move, EventPriority.HIGH)

    def on_before_get_move_options(self, event: BeforeGetMoveOptionsEvent):
        move_options = list(event.move_options)
        board = event.piece.board
        position = event.piece.position

        for move_option in move_options:
            move_position = move_option.position

            move_offset = (move_position.x - position.x, move_position.y - position.y)
            opposite_move_position = position.offset(-move_offset[0], -move_offset[1])

            if (
                is_in_board(board, opposite_move_position)
                and isinstance(board[opposite_move_position].piece, Queen)
                and board[opposite_move_position].piece.player != event.piece.player
            ):
                move_option.extra["la_bastarda"] = True
                move_option.extra["la_bastarda_position"] = position
                move_option.extra["la_bastarda_player"] = board[opposite_move_position].piece.player


        event.set_move_options(move_options)

    def on_after_move(self, event: AfterMoveEvent):
        if "la_bastarda" in event.move_option.extra:
            pawn = self._pawn(event.move_option.extra["la_bastarda_player"])
            la_bastarda_position = event.move_option.extra["la_bastarda_position"]
            event.piece.board[la_bastarda_position].piece = pawn

    def clone(self):
        return LaBastarda(pawn=self._pawn)
