from contextlib import contextmanager
from dataclasses import dataclass
from functools import partial
from typing import Iterable

from chessmaker.chess.base.board import AfterNewPieceEvent
from chessmaker.chess.base.move_option import MoveOption
from chessmaker.chess.base.piece import Piece, BeforeMoveEvent, BeforeGetMoveOptionsEvent
from chessmaker.chess.base.player import Player
from chessmaker.chess.base.position import Position
from chessmaker.chess.base.square import Square
from chessmaker.chess.piece_utils import filter_uncapturable_positions, is_in_board, iterate_until_blocked, \
    positions_to_move_options
from chessmaker.chess.pieces.rook import Rook
from chessmaker.events import Event, event_publisher, EventPriority


@dataclass(frozen=True)
class AfterCastleEvent(Event):
    king: "King"
    rook: Rook


@dataclass(frozen=True)
class BeforeCastleEvent(AfterCastleEvent):
    king_destination: Square
    rook_destination: Square

    def set_king_destination(self, king_destination: Square):
        self._set("king_destination", king_destination)

    def set_rook_destination(self, rook_destination: Square):
        self._set("rook_destination", rook_destination)


@event_publisher(AfterCastleEvent, BeforeCastleEvent)
class King(Piece):
    def __init__(
            self,
            player: Player,
            moved: bool = False,
            attackable: bool = False,
            castling_directions: tuple[tuple[int, int], ...] = ((1, 0), (-1, 0))
    ):
        super().__init__(player)
        self._moved = moved
        self._attackable = attackable
        self._castling_directions = castling_directions
        self.subscribe(BeforeMoveEvent, self._on_before_move, EventPriority.VERY_HIGH)

    @classmethod
    @property
    def name(cls):
        return "King"

    def on_join_board(self):
        super().on_join_board()
        if not self._attackable:
            for piece in self.board.get_pieces():
                if piece.player == self.player:
                    piece.subscribe(BeforeGetMoveOptionsEvent, self._on_before_get_move_options)
            self.board.subscribe(AfterNewPieceEvent, self._on_after_new_piece)

    def _on_after_new_piece(self, event: AfterNewPieceEvent):
        if event.piece.player == self.player:
            event.piece.subscribe(BeforeGetMoveOptionsEvent, self._on_before_get_move_options)

    def is_attacked(self) -> bool:
        for piece in self.board.get_pieces():
            if piece.player == self.player:
                continue

            move_options = piece.get_move_options()

            for move_option in move_options:
                if self.position in move_option.captures:
                    return True
        return False

    @contextmanager
    def _make_kings_attackable(self):
        previous_states = {}
        for piece in self.board.get_pieces():
            if isinstance(piece, King):
                previous_states[piece] = piece._attackable
                piece._attackable = True
        yield
        for piece, previous_state in previous_states.items():
            piece._attackable = previous_state

    def _is_attacked_after_move(self, piece: Piece, move_option: MoveOption) -> bool:
        with self._make_kings_attackable():
            board_clone = self.board.clone()
        self_clone = board_clone[self.position].piece
        piece_clone = board_clone[piece.position].piece
        piece_clone.move(move_option)
        return self_clone.is_attacked()

    def _on_before_get_move_options(self, event: BeforeGetMoveOptionsEvent):
        if event.piece.player != self.player:
            return

        if event.piece == self:
            move_options = list(event.move_options)

            for move_option in list(move_options):
                if "castling_with" in move_option.extra:
                    for position in range(self.position.x, move_option.position.x,
                                          1 if self.position.x < move_option.position.x else -1):
                        if self._is_attacked_after_move(self, MoveOption(Position(position, self.position.y))):
                            move_options.remove(move_option)
                            break
                else:
                    if self._is_attacked_after_move(self, move_option):
                        move_options.remove(move_option)

            event.set_move_options(move_options)
            return

        event_move_options = event.move_options
        move_options = []
        for move_option in event_move_options:
            if not self._is_attacked_after_move(event.piece, move_option):
                move_options.append(move_option)
        event.set_move_options(move_options)

    def _get_move_options(self) -> Iterable[MoveOption]:
        positions = [
            self.position.offset(1, 1), self.position.offset(1, 0), self.position.offset(1, -1),
            self.position.offset(0, -1), self.position.offset(-1, -1), self.position.offset(-1, 0),
            self.position.offset(-1, 1), self.position.offset(0, 1)
        ]

        positions = filter(partial(is_in_board, self.board), positions)
        positions = list(filter_uncapturable_positions(self, positions))

        move_options = list(positions_to_move_options(self.board, positions))

        for direction in self._castling_directions:
            line = list(iterate_until_blocked(self, direction))
            if len(line) > 2:
                last_piece = self.board[line[-1]].piece
                if (last_piece is not None and
                        last_piece.player == self.player and
                        isinstance(last_piece, Rook) and
                        not last_piece.moved and
                        not self._moved):
                    move_options.append(MoveOption(line[1], extra=dict(castle=line[-1])))

        return move_options

    def _on_before_move(self, event: BeforeMoveEvent):
        if "castle" in event.move_option.extra:
            move_option = event.move_option
            destination = self.board[move_option.position]

            rook_source = self.board[Position(*move_option.extra["castle"])]
            rook_destination = self.board[Position(
                (self.position.x + move_option.position.x) // 2,
                (self.position.y + move_option.position.y) // 2,
            )]
            rook: Rook = rook_source.piece

            before_castle_event = BeforeCastleEvent(self, rook, destination, rook_destination)
            self.publish(before_castle_event)

            before_castle_event.king_destination.piece = self
            self.board[self.position].piece = None
            self._moved = True

            before_castle_event.rook_destination.piece = rook
            rook_source.piece = None
            rook.moved = True

            self.publish(AfterCastleEvent(self, rook))
        self._moved = True

    def clone(self):
        return King(self.player, self._moved, attackable=self._attackable, castling_directions=self._castling_directions)
