import itertools
import warnings
from dataclasses import dataclass
from typing import Iterable, Iterator

from chessmaker.cloneable import Cloneable
from chessmaker.chess.base.piece import Piece, PIECE_EVENT_TYPES, AfterMoveEvent
from chessmaker.chess.base.player import Player
from chessmaker.chess.base.position import Position
from chessmaker.chess.base.rule import Rule
from chessmaker.chess.base.square import Square, SQUARE_EVENT_TYPES, AfterAddPieceEvent
from chessmaker.events import event_publisher, Event, CancellableEvent, EventPublisher, EventPriority


@dataclass(frozen=True)
class AfterNewPieceEvent(Event):
    piece: Piece


@dataclass(frozen=True)
class AfterRemoveSquareEvent(Event):
    position: Position
    square: Square


@dataclass(frozen=True)
class BeforeRemoveSquareEvent(AfterRemoveSquareEvent):
    pass


@dataclass(frozen=True)
class AfterAddSquareEvent(Event):
    position: Position
    square: Square


@dataclass(frozen=True)
class BeforeAddSquareEvent(AfterAddSquareEvent):
    def set_square(self, square: Square):
        self._set("square", square)


@dataclass(frozen=True)
class BeforeTurnChangeEvent(CancellableEvent):
    board: "Board"
    next_player: Player

    def set_next_player(self, next_player: Player):
        self._set("next_player", next_player)


@dataclass(frozen=True)
class AfterTurnChangeEvent(Event):
    board: "Board"
    player: Player


@event_publisher(*SQUARE_EVENT_TYPES, *PIECE_EVENT_TYPES, BeforeAddSquareEvent, AfterAddSquareEvent,
                 BeforeRemoveSquareEvent, AfterRemoveSquareEvent, BeforeTurnChangeEvent, AfterTurnChangeEvent,
                 AfterNewPieceEvent)
class Board(Cloneable, EventPublisher):
    def __init__(
            self,
            squares: list[list[Square | None]],
            players: list[Player],
            turn_iterator: Iterator[Player],
            rules: list[Rule] = None
    ):
        super().__init__()
        # Use the max length for each dimension to determine the size of the board
        self.size = (max(len(row) for row in squares), len(squares))
        self._squares = squares
        self._squares_to_positions = {square: Position(x, y) for y, row in enumerate(squares) for x, square in
                                      enumerate(row) if square is not None}
        self.players = players
        self.turn_iterator = turn_iterator
        self.current_player = next(self.turn_iterator)
        self.rules = rules or []

        # Subscribe to the events of each square
        for row in self._squares:
            for square in row:
                if square is not None:
                    # TODO: Subscribe to new squares
                    self.propagate_all(square)
                    square._board = self
                    if square.piece is not None:
                        self._on_after_add_piece(AfterAddPieceEvent(square, square.piece))

        self.subscribe(AfterAddPieceEvent, self._on_after_add_piece)
        self.subscribe(AfterMoveEvent, self._on_after_move, EventPriority.VERY_LOW)

        for rule in self.rules:
            rule.on_join_board(self)

    # TODO: Implement this in a way that detects actual new pieces and not moved pieces
    def _on_after_add_piece(self, event: AfterAddPieceEvent):
        piece: Piece = event.piece
        if piece._board is None:
            piece._board = self
            piece.on_join_board()
            self.publish(AfterNewPieceEvent(piece))
            self.propagate_all(piece)

    def _on_after_move(self, _: AfterMoveEvent):
        next_player = next(self.turn_iterator)
        before_turn_change_event = BeforeTurnChangeEvent(self, next_player)
        self.publish(before_turn_change_event)
        if before_turn_change_event.cancelled:
            return
        self.current_player = before_turn_change_event.next_player
        self.publish(AfterTurnChangeEvent(self, self.current_player))

    def __getitem__(self, position: Position) -> Square | None:
        return self._squares[position.y][position.x]

    def __setitem__(self, position: Position, square: Square | None):
        if square == self._squares[position.y][position.x]:
            warnings.warn("Setting a square to the same square doesn't have any effect, did you mean to to change "
                          "the piece on the square?", RuntimeWarning)
            return

        old_square = self._squares[position.y][position.x]
        if old_square is not None:
            self.publish(BeforeRemoveSquareEvent(position, old_square))

        if square is None:
            self._squares[position.y][position.x] = None
        else:
            before_add_square_event = BeforeAddSquareEvent(position, square)
            self.publish(before_add_square_event)
            self._squares[position.y][position.x] = before_add_square_event.square
            self._squares_to_positions[square] = position
            self.publish(AfterAddSquareEvent(position, square))

        if old_square is not None:
            self._squares_to_positions.pop(old_square)
            self.publish(AfterRemoveSquareEvent(position, old_square))

    def __iter__(self) -> Iterable[Square]:
        for row in self._squares:
            for square in row:
                if square is not None:
                    yield square

    def _get_piece_position(self, piece: Piece) -> Position:
        if piece is None:
            raise ValueError("Cannot get the position of a None piece")
        for y, row in enumerate(self._squares):
            for x, square in enumerate(row):
                if square is not None and square.piece == piece:
                    return Position(x, y)

    def _get_square_position(self, square: Square) -> Position:
        if square is None:
            raise ValueError("Cannot get the position of a None square")
        return self._squares_to_positions[square]

    def get_pieces(self) -> Iterable[Piece]:
        for square in self:
            if square.piece is not None:
                yield square.piece

    def get_player_pieces(self, player: Player) -> Iterable[Piece]:
        for piece in self.get_pieces():
            if piece.player == player:
                yield piece

    def clone(self):
        turn_iterators = itertools.tee(self.turn_iterator, 2)
        self.turn_iterator = turn_iterators[0]
        return Board(
            [[square.clone() if square is not None else None for square in row] for row in self._squares],
            self.players,
            itertools.chain([self.current_player], turn_iterators[1]),
            [rule.clone() for rule in self.rules]
        )
