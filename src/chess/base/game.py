from dataclasses import dataclass
from dataclasses import dataclass
from typing import Callable

from src.chess.base.board import Board, AfterTurnChangeEvent
from src.events import Event, EventPublisher


@dataclass(frozen=True)
class AfterGameEndEvent(Event):
    game: "Game"
    result: str

class Game(EventPublisher[AfterGameEndEvent]):
    def __init__(
            self,
            board: Board,
            get_result: Callable[[Board], str | None],
        ):
        super().__init__()
        self.board: Board = board
        self._get_result = get_result
        self.result = None

        self.board.subscribe(AfterTurnChangeEvent, self._on_after_turn_change)


    def _on_after_turn_change(self, _: AfterTurnChangeEvent):
        self.result = self._get_result(self.board)
        if self.result is not None:
            self.turn_iterator = []
            self.current_player = None
            self.publish(AfterGameEndEvent(self, self.result))

# TODO: Consider dependency injection, context variables, or flask-like globals
