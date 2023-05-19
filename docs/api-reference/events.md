<a id="chessmaker.events.event"></a>

# chessmaker.events.event

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/31277ef9b150ef22d5ea0caafe33d2906b6c7f48/chessmaker\events\event.py#L1)

<a id="chessmaker.events.event.Event"></a>

## Event

```python
@dataclass(frozen=True)
class Event()
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/31277ef9b150ef22d5ea0caafe33d2906b6c7f48/chessmaker\events\event.py#L5)

<a id="chessmaker.events.event.CancellableEvent"></a>

## CancellableEvent

```python
@dataclass(frozen=True)
class CancellableEvent(Event)
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/31277ef9b150ef22d5ea0caafe33d2906b6c7f48/chessmaker\events\event.py#L10)

<a id="chessmaker.events.event.CancellableEvent.cancelled"></a>

#### cancelled: `bool`

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/31277ef9b150ef22d5ea0caafe33d2906b6c7f48/chessmaker\events\event.py#L11)

<a id="chessmaker.events.event.CancellableEvent.set_cancelled"></a>

#### set\_cancelled

```python
def set_cancelled(cancelled: bool)
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/31277ef9b150ef22d5ea0caafe33d2906b6c7f48/chessmaker\events\event.py#L13)

<a id="chessmaker.events.event_priority"></a>

# chessmaker.events.event\_priority

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/31277ef9b150ef22d5ea0caafe33d2906b6c7f48/chessmaker\events\event_priority.py#L1)

<a id="chessmaker.events.event_priority.EventPriority"></a>

## EventPriority

```python
class EventPriority(int,  Enum)
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/31277ef9b150ef22d5ea0caafe33d2906b6c7f48/chessmaker\events\event_priority.py#L4)

<a id="chessmaker.events.event_priority.EventPriority.VERY_LOW"></a>

#### VERY\_LOW

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/31277ef9b150ef22d5ea0caafe33d2906b6c7f48/chessmaker\events\event_priority.py#L5)

<a id="chessmaker.events.event_priority.EventPriority.LOW"></a>

#### LOW

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/31277ef9b150ef22d5ea0caafe33d2906b6c7f48/chessmaker\events\event_priority.py#L6)

<a id="chessmaker.events.event_priority.EventPriority.NORMAL"></a>

#### NORMAL

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/31277ef9b150ef22d5ea0caafe33d2906b6c7f48/chessmaker\events\event_priority.py#L7)

<a id="chessmaker.events.event_priority.EventPriority.HIGH"></a>

#### HIGH

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/31277ef9b150ef22d5ea0caafe33d2906b6c7f48/chessmaker\events\event_priority.py#L8)

<a id="chessmaker.events.event_priority.EventPriority.VERY_HIGH"></a>

#### VERY\_HIGH

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/31277ef9b150ef22d5ea0caafe33d2906b6c7f48/chessmaker\events\event_priority.py#L9)

<a id="chessmaker.events.event_publisher"></a>

# chessmaker.events.event\_publisher

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/31277ef9b150ef22d5ea0caafe33d2906b6c7f48/chessmaker\events\event_publisher.py#L1)

<a id="chessmaker.events.event_publisher.EventPublisher"></a>

## EventPublisher

```python
class EventPublisher()
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/31277ef9b150ef22d5ea0caafe33d2906b6c7f48/chessmaker\events\event_publisher.py#L18)

<a id="chessmaker.events.event_publisher.EventPublisher.__init__"></a>

#### \_\_init\_\_

```python
def __init__(event_types: tuple[Type[Event], ...] = None)
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/31277ef9b150ef22d5ea0caafe33d2906b6c7f48/chessmaker\events\event_publisher.py#L19)

<a id="chessmaker.events.event_publisher.EventPublisher.subscribe"></a>

#### subscribe

```python
def subscribe(event_type: Type[TEvent], callback: Callable[[TEvent], None], priority: int = EventPriority.NORMAL)
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/31277ef9b150ef22d5ea0caafe33d2906b6c7f48/chessmaker\events\event_publisher.py#L27)

<a id="chessmaker.events.event_publisher.EventPublisher.unsubscribe"></a>

#### unsubscribe

```python
def unsubscribe(event_type: Type[TEvent], callback: Callable[[TEvent], None])
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/31277ef9b150ef22d5ea0caafe33d2906b6c7f48/chessmaker\events\event_publisher.py#L34)

<a id="chessmaker.events.event_publisher.EventPublisher.subscribe_to_all"></a>

#### subscribe\_to\_all

```python
def subscribe_to_all(callback: Callable[[Event], None], priority: int = EventPriority.NORMAL)
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/31277ef9b150ef22d5ea0caafe33d2906b6c7f48/chessmaker\events\event_publisher.py#L38)

<a id="chessmaker.events.event_publisher.EventPublisher.unsubscribe_from_all"></a>

#### unsubscribe\_from\_all

```python
def unsubscribe_from_all(callback: Callable[[Event], None])
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/31277ef9b150ef22d5ea0caafe33d2906b6c7f48/chessmaker\events\event_publisher.py#L42)

<a id="chessmaker.events.event_publisher.EventPublisher.publish"></a>

#### publish

```python
def publish(event: Event)
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/31277ef9b150ef22d5ea0caafe33d2906b6c7f48/chessmaker\events\event_publisher.py#L46)

<a id="chessmaker.events.event_publisher.EventPublisher.propagate"></a>

#### propagate

```python
def propagate(publisher: 'EventPublisher', event_type: Type[Event])
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/31277ef9b150ef22d5ea0caafe33d2906b6c7f48/chessmaker\events\event_publisher.py#L50)

For all events publisher publishes of type event_type, publish them to self

<a id="chessmaker.events.event_publisher.EventPublisher.propagate_all"></a>

#### propagate\_all

```python
def propagate_all(publisher: 'EventPublisher')
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/31277ef9b150ef22d5ea0caafe33d2906b6c7f48/chessmaker\events\event_publisher.py#L58)

For all events publisher publishes, publish them to self

<a id="chessmaker.events.event_publisher.event_publisher"></a>

#### event\_publisher

```python
def event_publisher(*event_types: Type[Event]) -> Callable[[Type[T]], Type[T] | Type[EventPublisher]]
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/31277ef9b150ef22d5ea0caafe33d2906b6c7f48/chessmaker\events\event_publisher.py#L69)

