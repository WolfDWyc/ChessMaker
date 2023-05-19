from typing import Iterable

from chessmaker.chess.base import Player
from chessmaker.chess.base.move_option import MoveOption
from chessmaker.chess.base.piece import Piece, BeforeGetMoveOptionsEvent
from chessmaker.events import EventPriority


class Duck(Piece):
    def __init__(self, player: Player, movable: bool = False):
        super().__init__(player)
        self.movable = movable

    @classmethod
    @property
    def name(cls):
        return "Duck"

    def on_join_board(self):
        self.board.subscribe(BeforeGetMoveOptionsEvent, self._on_before_get_move_options, EventPriority.HIGH)

    def _on_before_get_move_options(self, event: BeforeGetMoveOptionsEvent):
        if self.movable:
            if event.piece is not self:
                event.set_move_options([])

    def _get_move_options(self) -> Iterable[MoveOption]:
        if self.movable:
            for square in self.board:
                if square.piece is None and square.position != self.position:
                    yield MoveOption(square.position)

    def clone(self):
        return Duck(self.player, movable=self.movable)
