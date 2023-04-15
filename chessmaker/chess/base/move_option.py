from dataclasses import dataclass, field

from chessmaker.chess.base.position import Position


@dataclass
class MoveOption:
    position: Position
    captures: set[Position] = field(default_factory=set)
    extra: dict[str, any] = field(default_factory=dict)


