from functools import partial
from typing import Iterable

from src.chess.base.move_option import MoveOption
from src.chess.base.piece import Piece
from src.chess.pieces.piece_utils import filter_uncapturable_positions, is_in_board, positions_to_move_options

MOVE_OFFSETS = [(1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)]


class Knight(Piece):
    @classmethod
    @property
    def name(cls):
        return "Knight"

    def _get_move_options(self) -> Iterable[MoveOption]:
        positions = [self.position.offset(*offset) for offset in MOVE_OFFSETS]
        positions = filter(partial(is_in_board, self.board), positions)
        positions = filter_uncapturable_positions(self, positions)
        return positions_to_move_options(self.board, positions)

    def clone(self):
        return Knight(self.player)
