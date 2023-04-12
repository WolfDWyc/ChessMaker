from functools import partial

from src.chess.base.piece import AfterMoveEvent
from src.chess.pieces import knight
from src.chess.pieces.knight import Knight
from src.chess.pieces.knook import merge_to_knook
from src.chess.pieces.knook.knookable import Knookable
from src.chess.pieces.piece_utils import is_in_board
from src.events import EventPriority


class KnookableKnight(Knight, Knookable):
    def __init__(self, player):
        super().__init__(player)
        self.subscribe(AfterMoveEvent, merge_to_knook.on_after_move, EventPriority.VERY_HIGH)

    def _get_move_options(self):
        positions = [self.position.offset(*offset) for offset in knight.MOVE_OFFSETS]
        positions = list(filter(partial(is_in_board, self.board), positions))
        merge_move_options = merge_to_knook.get_merge_move_options(self, positions)

        return list(super()._get_move_options()) + list(merge_move_options)

    def clone(self):
        return KnookableKnight(self.player)
