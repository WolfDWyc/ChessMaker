from functools import partial
from itertools import chain

from chessmaker.chess.base.piece import AfterMoveEvent
from chessmaker.chess.pieces import knight
from chessmaker.chess.pieces.knight import Knight
from chessmaker.chess.pieces.knook.knookable import Knookable
from chessmaker.chess.piece_utils import is_in_board
from chessmaker.chess.pieces.knook.merge_to_knook import get_merge_move_options, merge_after_move, \
    MERGE_TO_KNOOK_EVENT_TYPES
from chessmaker.events import EventPriority, event_publisher


@event_publisher(*MERGE_TO_KNOOK_EVENT_TYPES)
class KnookableKnight(Knight, Knookable):
    def __init__(self, player):
        super().__init__(player)
        self.subscribe(AfterMoveEvent, merge_after_move, EventPriority.VERY_HIGH)

    def _get_move_options(self):
        positions = [self.position.offset(*offset) for offset in knight.MOVE_OFFSETS]
        positions = list(filter(partial(is_in_board, self.board), positions))
        merge_move_options = get_merge_move_options(self, positions)

        return chain(super()._get_move_options(), merge_move_options)

    def clone(self):
        return KnookableKnight(self.player)
