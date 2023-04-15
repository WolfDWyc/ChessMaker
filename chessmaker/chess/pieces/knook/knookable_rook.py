from itertools import chain
from typing import Iterable

from chessmaker.chess.base.move_option import MoveOption
from chessmaker.chess.base.piece import AfterMoveEvent, PieceEventTypes
from chessmaker.chess.base.player import Player
from chessmaker.chess.pieces.knook import merge_to_knook
from chessmaker.chess.pieces.knook.knookable import Knookable
from chessmaker.chess.piece_utils import get_straight_until_blocked
from chessmaker.chess.pieces.rook import Rook
from chessmaker.events import EventPriority, EventPublisher


class KnookableRook(Rook, EventPublisher[PieceEventTypes | merge_to_knook.MergeToKnookEventTypes], Knookable):
    def __init__(self, player: Player, moved: bool = False):
        super().__init__(player, moved)
        self.subscribe(AfterMoveEvent, merge_to_knook.on_after_move, EventPriority.VERY_HIGH)

    def _get_move_options(self) -> Iterable[MoveOption]:
        positions = list(get_straight_until_blocked(self))
        merge_move_options = merge_to_knook.get_merge_move_options(self, positions)

        return chain(super()._get_move_options(), merge_move_options)

    def clone(self):
        return KnookableRook(self.player, self.moved)
