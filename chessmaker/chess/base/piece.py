from abc import abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING, Iterable

from chessmaker.chess.base.move_option import MoveOption
from chessmaker.chess.base.player import Player
from chessmaker.cloneable import Cloneable
from chessmaker.events import event_publisher, Event, CancellableEvent, EventPublisher

if TYPE_CHECKING:
    from chessmaker.chess.base.board import Board


@dataclass(frozen=True)
class AfterGetMoveOptionsEvent(Event):
    piece: "Piece"
    move_options: Iterable[MoveOption]


class BeforeGetMoveOptionsEvent(AfterGetMoveOptionsEvent):
    def set_move_options(self, move_options: Iterable[MoveOption]):
        self._set("move_options", move_options)


@dataclass(frozen=True)
class AfterMoveEvent(Event):
    piece: "Piece"
    move_option: MoveOption


class BeforeMoveEvent(AfterMoveEvent, CancellableEvent):
    def set_move_option(self, move_option: MoveOption):
        self._set("move_option", move_option)


@dataclass(frozen=True)
class AfterCapturedEvent(Event):
    captured_piece: "Piece"


class BeforeCapturedEvent(AfterCapturedEvent):
    pass


PIECE_EVENT_TYPES = (BeforeGetMoveOptionsEvent, AfterGetMoveOptionsEvent, BeforeMoveEvent, AfterMoveEvent,
                     BeforeCapturedEvent, AfterCapturedEvent)


@event_publisher(*PIECE_EVENT_TYPES)
class Piece(Cloneable, EventPublisher):
    def __init__(self, player: Player):
        super().__init__()
        self.player = player
        self._board: Board = None

    def __repr__(self):
        return f"{self.__class__.__name__} ({self.player})"

    def get_move_options(self) -> Iterable[MoveOption]:
        move_options = self._get_move_options()

        before_get_move_options_event = BeforeGetMoveOptionsEvent(self, move_options)
        self.publish(before_get_move_options_event)
        move_options = before_get_move_options_event.move_options
        self.publish(AfterGetMoveOptionsEvent(self, move_options))

        return move_options

    def move(self, move_option: MoveOption):
        before_move_event = BeforeMoveEvent(self, move_option)
        self.publish(before_move_event)
        if before_move_event.cancelled:
            return

        move_option = before_move_event.move_option

        source = self.board[self.position]
        source.piece = None

        destination = self.board[move_option.position]

        for capture_position in move_option.captures:
            capture_piece = self.board[capture_position].piece
            capture_piece.publish(BeforeCapturedEvent(capture_piece))
            self.board[capture_position].piece = None
            capture_piece.publish(AfterCapturedEvent(capture_piece))

        destination.piece = self

        self.publish(AfterMoveEvent(self, move_option))

    def on_join_board(self):
        pass

    @property
    def position(self):
        return self.board._get_piece_position(self)

    @property
    def board(self):
        if self._board is None:
            raise Exception("Piece is not on the board yet")
        return self._board

    @classmethod
    @property
    @abstractmethod
    def name(cls):
        raise NotImplementedError

    @abstractmethod
    def _get_move_options(self) -> Iterable[MoveOption]:
        raise NotImplementedError

    @abstractmethod
    def clone(self):
        raise NotImplementedError
