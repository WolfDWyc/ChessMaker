import warnings
from dataclasses import dataclass
from typing import TYPE_CHECKING

from chessmaker.chess.base.piece import Piece
from chessmaker.cloneable import Cloneable
from chessmaker.events import Event, EventPublisher

if TYPE_CHECKING:
    from chessmaker.chess.base.board import Board

@dataclass(frozen=True)
class AfterAddPieceEvent(Event):
    square: "Square"
    piece: Piece

class BeforeAddPieceEvent(AfterAddPieceEvent):
    def set_piece(self, piece: Piece):
        self._set("piece", piece)

@dataclass(frozen=True)
class BeforeRemovePieceEvent(Event):
    square: "Square"
    piece: Piece

class AfterRemovePieceEvent(BeforeRemovePieceEvent):
    pass


class Square(EventPublisher[BeforeAddPieceEvent | AfterAddPieceEvent | BeforeRemovePieceEvent | AfterRemovePieceEvent], Cloneable):
    def __init__(self, piece: Piece | None = None):
        super().__init__()
        self._piece = piece
        self.board: Board = None

    @property
    def piece(self) -> Piece:
        return self._piece

    @property
    def position(self):
        return self.board._get_square_position(self)

    @piece.setter
    def piece(self, piece: Piece):
        old_piece = self._piece

        if piece is old_piece:
            warnings.warn("Setting the same piece on the square has no effect", RuntimeWarning)
            return

        if old_piece is not None:
            self.publish(BeforeRemovePieceEvent(self, old_piece))

        if piece is None:
            self._piece = None
        else:
            before_add_piece_event = BeforeAddPieceEvent(self, piece)
            self.publish(before_add_piece_event)
            self._piece = before_add_piece_event.piece
            self.publish(AfterAddPieceEvent(self, self._piece))

        if old_piece is not None:
            self.publish(AfterRemovePieceEvent(self, old_piece))

    def clone(self):
        return Square(self.piece.clone() if self.piece is not None else None)
