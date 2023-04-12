import bisect
from collections import defaultdict
from dataclasses import dataclass, field
from typing import TypeVar, Callable, Generic, Type

from chessmaker.events.event import Event
from chessmaker.events.event_priority import EventPriority


@dataclass(frozen=True)
class _Subscriber:
    callback: Callable[[Event], None]
    priority: int = field(default=EventPriority.NORMAL, compare=False, hash=False)
TEvent = TypeVar('TEvent', bound=Event)

class EventPublisher(Generic[TEvent]):
    def __init__(self,
                 subscribers: dict[Type[TEvent], list[_Subscriber]] = None,
                subscribers_to_all: list[_Subscriber] = None
         ):
        if subscribers is None:
            subscribers = defaultdict(list)
        if subscribers_to_all is None:
            subscribers_to_all = defaultdict(list)
        self._subscribers: dict[Type[TEvent], list[_Subscriber]] = subscribers
        self._subscribers_to_all: dict[_Subscriber, list[Type[TEvent]]] = subscribers_to_all

    def subscribe(self, event_type: Type[TEvent], callback: Callable[[TEvent], None], priority: int = EventPriority.NORMAL):
        bisect.insort(self._subscribers[event_type], _Subscriber(callback, priority), key=lambda subscriber: -subscriber.priority)


    def unsubscribe(self, event_type: Type[TEvent], callback: Callable[[TEvent], None]):
        while callback in self._subscribers[event_type]:
            self._subscribers[event_type].remove(_Subscriber(callback))

    def subscribe_to_all(self, callback: Callable[[TEvent], None], priority: int = EventPriority.NORMAL):
        for event_type in self._subscribers:
            self.subscribe(event_type, callback, priority)
        self._subscribers_to_all[_Subscriber(callback, priority)] = list(self._subscribers.keys())

    def unsubscribe_from_all(self, callback: Callable[[TEvent], None]):
        for event_type in self._subscribers:
            self.unsubscribe(event_type, callback)
        self._subscribers_to_all.pop(_Subscriber(callback))

    def publish(self, event: TEvent):
        event_type = type(event)
        for subscriber, event_types in self._subscribers_to_all.items():
            if event_type not in event_types:
                self.subscribe(event_type, subscriber.callback, subscriber.priority)
                self._subscribers_to_all[subscriber].append(event_type)
        for subscriber in self._subscribers[type(event)]:
            subscriber.callback(event)


    def propagate(self, publisher: 'EventPublisher', event_type: Type[TEvent], priority: int = EventPriority.NORMAL):
        """
        For all events publisher publishes of type event_type, publish them to self
        """
        def callback(event: TEvent):
            self.publish(event)

        publisher.subscribe(event_type, callback, priority)

    def propagate_all(self, publisher: 'EventPublisher', priority: int = EventPriority.NORMAL):
        """
        For all events publisher publishes, publish them to self
        """
        def callback(event: TEvent):
            self.publish(event)

        publisher.subscribe_to_all(callback, priority)
