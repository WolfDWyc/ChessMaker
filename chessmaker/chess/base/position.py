from typing import NamedTuple


class Position(NamedTuple):
    x: int
    y: int

    def __str__(self):
        return f"{self.x}-{self.y}"

    def offset(self, x: int, y: int):
        return Position(self.x + x, self.y + y)
