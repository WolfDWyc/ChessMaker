import dataclasses
from dataclasses import dataclass
from enum import Enum
from typing import Iterable, Type

from src.chess.base.board import AfterNewPieceEvent
from src.chess.base.game import AfterTurnChangeEvent
from src.chess.base.move_option import MoveOption
from src.chess.base.piece import Piece, BeforeMoveEvent, AfterMoveEvent, BeforeCaptureEvent, AfterCaptureEvent
from src.chess.base.player import Player
from src.chess.base.position import Position
from src.chess.pieces.piece_utils import iterate_until_blocked, is_in_board
from src.events import EventPriority, Event

@dataclass(frozen=True)
class AfterPromotionEvent(Event):
    pawn: "Pawn"
    promotion: Piece

@dataclass(frozen=True)
class BeforePromotionEvent(AfterPromotionEvent):
    def set_promotion(self, promotion: Piece):
        self._set("promotion", promotion)

class Pawn(Piece):
    class Direction(Enum):
        UP = -1
        DOWN = 1

    @classmethod
    @property
    def name(cls):
        return "Pawn"

    def __init__(
            self,
            player: Player,
            direction: Direction,
            promotions: Iterable[Type[Piece]] = None,
            moved_turns_ago: int = -1,
            last_position: Position = None
    ):
        super().__init__(player)
        if promotions is None:
            promotions = []
        self.promotions = {promotion.name: promotion for promotion in promotions}
        self._direction = direction
        self._moved_turns_ago = moved_turns_ago
        self._last_position = last_position

        self.subscribe(AfterNewPieceEvent, self.on_after_added_to_board)
        self.subscribe(BeforeMoveEvent, self._on_before_move, EventPriority.VERY_HIGH)
        self.subscribe(AfterMoveEvent, self._on_after_move, EventPriority.VERY_HIGH)

    def on_after_added_to_board(self):
        self.board.subscribe(AfterTurnChangeEvent, self._on_turn_change)

    def _on_turn_change(self, _: AfterTurnChangeEvent):
        if self._moved_turns_ago != -1:
            self._moved_turns_ago += 1

    def _get_move_options(self) -> Iterable[MoveOption]:
        move_options = []
        non_capture_reach = 2 if self._moved_turns_ago == -1 else 1
        non_capture_positions = list(iterate_until_blocked(self, (0, self._direction.value)))[:non_capture_reach]
        if len(non_capture_positions) != 0 and self.board[non_capture_positions[-1]].piece is not None:
            non_capture_positions.pop()
        move_options += [MoveOption(position) for position in non_capture_positions]

        capture_positions = [self.position.offset(1, self._direction.value),
                             self.position.offset(-1, self._direction.value)]
        capture_positions = filter(lambda position: is_in_board(self.board, position), capture_positions)

        for position in capture_positions:
            position_piece = self.board[position].piece
            if position_piece is None:
                above_position, below_position = Position(position.x, position.y + 1), Position(position.x, position.y - 1)
                if not is_in_board(self.board, above_position) or not is_in_board(self.board, below_position):
                    continue
                squares = self.board[above_position], self.board[below_position]

                for i, square in enumerate(squares):
                    if (square is not None
                            and isinstance(square.piece, Pawn)
                            and square.piece.player != self.player
                            and square.piece._last_position == squares[1 - i].position
                            and 0 <= square.piece._moved_turns_ago <= 1):
                        move_options.append(MoveOption(position, extra=dict(en_passant=True), captures={square.position}))
                continue
            elif position_piece.player == self.player:
                continue
            move_options.append(MoveOption(position, captures={position}))

        for move_option in list(move_options):
            position = move_option.position
            last_position_in_column = max(filter(lambda square: square.position.x == position.x, self.board),
                                          key=lambda square: square.position.y * self._direction.value).position
            if position == last_position_in_column:
                move_options.remove(move_option)
                for promotion_name in self.promotions:
                    move_options.append(dataclasses.replace(move_option, extra=dict(promote=promotion_name)))

        return move_options


    def _on_before_move(self, _: BeforeMoveEvent):
        self._last_position = self.position

    def _on_after_move(self, event: AfterMoveEvent):
        self._moved_turns_ago = 0
        move_option = event.move_option

        if "promote" in move_option.extra:
            new_piece = self.promotions[move_option.extra["promote"]](self.player)
            before_promotion_event = BeforePromotionEvent(self, new_piece)
            self.publish(before_promotion_event)
            self.board[self.position].piece = before_promotion_event.promotion
            self.publish(AfterPromotionEvent(self, before_promotion_event.promotion))

    def clone(self):
        return Pawn(self.player, self._direction, list(self.promotions.values()), self._moved_turns_ago, self._last_position)
