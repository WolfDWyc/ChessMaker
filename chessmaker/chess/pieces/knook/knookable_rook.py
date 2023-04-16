from itertools import chain
from typing import Iterable

from chessmaker.chess.base.move_option import MoveOption
from chessmaker.chess.base.piece import AfterMoveEvent
from chessmaker.chess.base.player import Player
from chessmaker.chess.pieces.knook.knookable import Knookable
from chessmaker.chess.piece_utils import get_straight_until_blocked
from chessmaker.chess.pieces.knook.merge_to_knook import get_merge_move_options, MERGE_TO_KNOOK_EVENT_TYPES, \
    merge_after_move
from chessmaker.chess.pieces.rook import Rook
from chessmaker.events import EventPriority, event_publisher


@event_publisher(*MERGE_TO_KNOOK_EVENT_TYPES)
class KnookableRook(Rook, Knookable):
    def __init__(self, player: Player, moved: bool = False):
        super().__init__(player, moved)
        self.subscribe(AfterMoveEvent, merge_after_move, EventPriority.VERY_HIGH)

    def _get_move_options(self) -> Iterable[MoveOption]:
        positions = list(get_straight_until_blocked(self))
        merge_move_options = get_merge_move_options(self, positions)

        return chain(super()._get_move_options(), merge_move_options)

    def clone(self):
        return KnookableRook(self.player, self.moved)
