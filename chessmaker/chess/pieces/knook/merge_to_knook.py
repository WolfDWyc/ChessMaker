from dataclasses import dataclass
from typing import Iterable

from chessmaker.chess.base.move_option import MoveOption
from chessmaker.chess.base.piece import Piece, AfterMoveEvent
from chessmaker.chess.base.position import Position
from chessmaker.chess.pieces.knook.knook import Knook
from chessmaker.chess.pieces.knook.knookable import Knookable
from chessmaker.events import Event


@dataclass(frozen=True)
class AfterMergeToKnookEvent(Event):
    piece: Piece
    knook: Knook

class BeforeMergeToKnookEvent(AfterMergeToKnookEvent):
    def set_knook(self, knook: Knook):
        self._set("knook", knook)


def get_merge_move_options(piece: Piece, positions: Iterable[Position]) -> Iterable[MoveOption]:
    for position in positions:
        position_piece = piece.board[position].piece

        if position_piece is not None and position_piece.player == piece.player:
            if isinstance(position_piece, Knookable) and not isinstance(position_piece, type(piece)):
                yield MoveOption(position, extra=dict(knook=True))

def on_after_move(event: AfterMoveEvent):
    if "knook" in event.move_option.extra:
        piece = event.piece
        before_merge_to_knook_event = BeforeMergeToKnookEvent(piece, Knook(event.piece.player))
        event.piece.publish(before_merge_to_knook_event)
        knook = before_merge_to_knook_event.knook
        piece.board[event.move_option.position].piece = knook
        piece.publish(AfterMergeToKnookEvent(piece, knook))



