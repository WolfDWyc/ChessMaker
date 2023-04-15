from typing import Iterable

from chessmaker.chess.base.move_option import MoveOption
from chessmaker.chess.base.piece import Piece
from chessmaker.chess.piece_utils import get_diagonals_until_blocked, filter_uncapturable_positions, \
    positions_to_move_options


class Bishop(Piece):
    @classmethod
    @property
    def name(cls):
        return "Bishop"

    def _get_move_options(self) -> Iterable[MoveOption]:
        positions = filter_uncapturable_positions(self, get_diagonals_until_blocked(self))
        return positions_to_move_options(self.board, positions)

    def clone(self):
        return Bishop(self.player)
