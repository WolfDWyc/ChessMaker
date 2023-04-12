from dataclasses import dataclass, field

from src.chess.base.position import Position


@dataclass
class MoveOption:
    position: Position
    extra: dict[str, any] = field(default_factory=dict)
    captures: set[Position] = field(default_factory=set)


