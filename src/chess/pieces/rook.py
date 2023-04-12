from typing import Iterable

from src.chess.base.move_option import MoveOption
from src.chess.base.piece import Piece, AfterMoveEvent
from src.chess.base.player import Player
from src.chess.pieces.piece_utils import filter_uncapturable_positions, get_straight_until_blocked, \
    positions_to_move_options
from src.events import EventPriority


class Rook(Piece):
    def __init__(self, player: Player, moved: bool = False):
        super().__init__(player)
        self.moved = moved
        self.subscribe(AfterMoveEvent, self._on_after_move, EventPriority.VERY_HIGH)

    @classmethod
    @property
    def name(cls):
        return "Rook"

    def _get_move_options(self) -> Iterable[MoveOption]:
        positions = filter_uncapturable_positions(self, get_straight_until_blocked(self))
        return positions_to_move_options(self.board, positions)

    def _on_after_move(self, _: AfterMoveEvent):
        self.moved = True

    def clone(self):
        return Rook(self.player, self.moved)
