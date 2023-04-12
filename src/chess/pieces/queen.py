from itertools import chain
from typing import Iterable

from src.chess.base.move_option import MoveOption
from src.chess.base.piece import Piece
from src.chess.pieces.piece_utils import filter_uncapturable_positions, get_straight_until_blocked \
    , get_diagonals_until_blocked, positions_to_move_options


class Queen(Piece):
    @classmethod
    @property
    def name(cls):
        return "Queen"

    def _get_move_options(self) -> Iterable[MoveOption]:
        positions = filter_uncapturable_positions(self, chain(
            get_straight_until_blocked(self),
            get_diagonals_until_blocked(self)
        ))
        return positions_to_move_options(self.board, positions)

    def clone(self):
        return Queen(self.player)
