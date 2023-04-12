from dataclasses import dataclass, field


@dataclass(frozen=True)
class Event:
    def _set(self, field: str, value: any):
        object.__setattr__(self, field, value)

@dataclass(frozen=True)
class CancellableEvent(Event):
    cancelled: bool = field(default=False, init=False)

    def set_cancelled(self, cancelled: bool):
        self._set("cancelled", cancelled)
