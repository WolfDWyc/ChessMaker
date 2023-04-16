import bisect
from dataclasses import dataclass, field
from typing import TypeVar, Callable, Type, cast

from chessmaker.events.event import Event
from chessmaker.events.event_priority import EventPriority


@dataclass(frozen=True)
class _Subscriber:
    callback: Callable[[Event], None]
    priority: int = field(default=EventPriority.NORMAL, compare=False, hash=False)


TEvent = TypeVar("TEvent", bound=Event)


class EventPublisher:
    def __init__(self, event_types: tuple[Type[Event], ...] = None):
        if event_types is not None:
            self._subscribers: dict[Type[Event], list[_Subscriber]] = {}
            self._propagating_to: dict[Type[Event], list[EventPublisher]] = {}
            for event_type in event_types:
                self._subscribers[event_type] = []
                self._propagating_to[event_type] = []

    def subscribe(self, event_type: Type[TEvent], callback: Callable[[TEvent], None],
                  priority: int = EventPriority.NORMAL):
        bisect.insort(self._subscribers[event_type], _Subscriber(callback, priority),
                      key=lambda subscriber: -subscriber.priority)
        for publisher in self._propagating_to[event_type]:
            publisher.subscribe(event_type, callback, priority)

    def unsubscribe(self, event_type: Type[TEvent], callback: Callable[[TEvent], None]):
        while callback in self._subscribers[event_type]:
            self._subscribers[event_type].remove(_Subscriber(callback))

    def subscribe_to_all(self, callback: Callable[[Event], None], priority: int = EventPriority.NORMAL):
        for event_type in self._subscribers.keys():
            self.subscribe(event_type, callback, priority)

    def unsubscribe_from_all(self, callback: Callable[[Event], None]):
        for event_type in self._subscribers.keys():
            self.unsubscribe(event_type, callback)

    def publish(self, event: Event):
        for subscriber in self._subscribers[type(event)]:
            subscriber.callback(event)

    def propagate(self, publisher: 'EventPublisher', event_type: Type[Event]):
        """
        For all events publisher publishes of type event_type, publish them to self
        """
        self._propagating_to[event_type].append(publisher)

    def propagate_all(self, publisher: 'EventPublisher'):
        """
        For all events publisher publishes, publish them to self
        """
        for event_type in (set(publisher._subscribers.keys()) & set(self._propagating_to.keys())):
            self.propagate(publisher, event_type)


T = TypeVar('T')


def event_publisher(*event_types: Type[Event]) -> Callable[[Type[T]], Type[T] | Type[EventPublisher]]:
    def _class(cls: Type[T]) -> Type[T] | Type[EventPublisher]:
        original_init = cls.__init__

        def __init__(self, *args, **kwargs):
            if hasattr(self, "_subscribers") and self._subscribers:
                EventPublisher.__init__(self, tuple(self._subscribers.keys()) + event_types)
            else:
                EventPublisher.__init__(self, event_types)

            original_init(self, *args, **kwargs)

        cls.__init__ = __init__
        cls.subscribe = EventPublisher.subscribe
        cls.unsubscribe = EventPublisher.unsubscribe
        cls.subscribe_to_all = EventPublisher.subscribe_to_all
        cls.unsubscribe_from_all = EventPublisher.unsubscribe_from_all
        cls.publish = EventPublisher.publish
        cls.propagate = EventPublisher.propagate
        cls.propagate_all = EventPublisher.propagate_all

        return cast(Type[EventPublisher], cls)

    return _class
