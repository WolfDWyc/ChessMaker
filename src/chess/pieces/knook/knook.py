from functools import partial
from typing import Iterable

from src.chess.base.move_option import MoveOption
from src.chess.base.piece import Piece
from src.chess.pieces import knight
from src.chess.pieces.piece_utils import filter_uncapturable_positions, is_in_board, \
    get_straight_until_blocked, positions_to_move_options


class Knook(Piece):
    @classmethod
    @property
    def name(cls):
        return "Knook"

    def _get_move_options(self) -> Iterable[MoveOption]:
        positions = [self.position.offset(*offset) for offset in knight.MOVE_OFFSETS]
        positions = filter(partial(is_in_board, self.board), positions)
        positions = filter_uncapturable_positions(self, positions)

        positions += filter_uncapturable_positions(self, get_straight_until_blocked(self))

        return positions_to_move_options(self.board, positions)

    def clone(self):
        return Knook(self.player)
