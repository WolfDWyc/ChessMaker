from abc import abstractmethod
from abc import abstractmethod
from typing import TYPE_CHECKING, Callable, Type

from src.cloneable import Cloneable

if TYPE_CHECKING:
    from src.chess.base.board import Board

class Rule(Cloneable):
    @abstractmethod
    def on_join_board(self, board: "Board"):
        raise NotImplementedError

    @abstractmethod
    def clone(self):
        raise NotImplementedError


def as_rule(rule_func: Callable[["Board"], None]) -> Type[Rule]:
    class RuleWrapper(Rule):
        def on_join_board(self, board: "Board"):
            rule_func(board)

        def clone(self):
            return RuleWrapper()

    return RuleWrapper
