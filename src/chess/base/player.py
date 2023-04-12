from dataclasses import dataclass, field
from uuid import uuid4


@dataclass(frozen=True)
class Player:
    name: str = field(default="", compare=False)
    # We compare by ID such that even if the player is deep copied only in some places, the comparison will still work
    # We don't compare by name because we want to allow two players with the same name
    # TODO: Do players even need a name? Maybe we should just use the ID
    _id: str = field(default_factory=lambda: str(uuid4()), compare=True)

    def __repr__(self):
        return f"Player ({self.name})"
