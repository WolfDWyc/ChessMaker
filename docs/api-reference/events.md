<a id="src.events.event"></a>

# src.events.event

<a id="src.events.event.Event"></a>

## Event

```python
@dataclass(frozen=True)
class Event()
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/fa904e10464b6e4f95136eb8c6d988f269e3f1a5/src\events\event.py#L5)

<a id="src.events.event.CancellableEvent"></a>

## CancellableEvent

```python
@dataclass(frozen=True)
class CancellableEvent(Event)
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/fa904e10464b6e4f95136eb8c6d988f269e3f1a5/src\events\event.py#L10)

<a id="src.events.event.CancellableEvent.cancelled"></a>

#### cancelled: `bool`

<a id="src.events.event.CancellableEvent.set_cancelled"></a>

#### set\_cancelled

```python
def set_cancelled(cancelled: bool)
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/fa904e10464b6e4f95136eb8c6d988f269e3f1a5/src\events\event.py#L13)

<a id="src.events.event_priority"></a>

# src.events.event\_priority

<a id="src.events.event_priority.EventPriority"></a>

## EventPriority

```python
class EventPriority(int, Enum)
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/fa904e10464b6e4f95136eb8c6d988f269e3f1a5/src\events\event_priority.py#L4)

<a id="src.events.event_priority.EventPriority.VERY_LOW"></a>

#### VERY\_LOW

<a id="src.events.event_priority.EventPriority.LOW"></a>

#### LOW

<a id="src.events.event_priority.EventPriority.NORMAL"></a>

#### NORMAL

<a id="src.events.event_priority.EventPriority.HIGH"></a>

#### HIGH

<a id="src.events.event_priority.EventPriority.VERY_HIGH"></a>

#### VERY\_HIGH

<a id="src.events.event_publisher"></a>

# src.events.event\_publisher

<a id="src.events.event_publisher.EventPublisher"></a>

## EventPublisher

```python
class EventPublisher(Generic[TEvent])
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/fa904e10464b6e4f95136eb8c6d988f269e3f1a5/src\events\event_publisher.py#L16)

<a id="src.events.event_publisher.EventPublisher.__init__"></a>

#### \_\_init\_\_

```python
def __init__(subscribers: dict[Type[TEvent], list[_Subscriber]] = None,
             subscribers_to_all: list[_Subscriber] = None)
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/fa904e10464b6e4f95136eb8c6d988f269e3f1a5/src\events\event_publisher.py#L17)

<a id="src.events.event_publisher.EventPublisher.subscribe"></a>

#### subscribe

```python
def subscribe(event_type: Type[TEvent],
              callback: Callable[[TEvent], None],
              priority: int = EventPriority.NORMAL)
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/fa904e10464b6e4f95136eb8c6d988f269e3f1a5/src\events\event_publisher.py#L28)

<a id="src.events.event_publisher.EventPublisher.unsubscribe"></a>

#### unsubscribe

```python
def unsubscribe(event_type: Type[TEvent], callback: Callable[[TEvent], None])
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/fa904e10464b6e4f95136eb8c6d988f269e3f1a5/src\events\event_publisher.py#L32)

<a id="src.events.event_publisher.EventPublisher.subscribe_to_all"></a>

#### subscribe\_to\_all

```python
def subscribe_to_all(callback: Callable[[TEvent], None],
                     priority: int = EventPriority.NORMAL)
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/fa904e10464b6e4f95136eb8c6d988f269e3f1a5/src\events\event_publisher.py#L36)

<a id="src.events.event_publisher.EventPublisher.unsubscribe_from_all"></a>

#### unsubscribe\_from\_all

```python
def unsubscribe_from_all(callback: Callable[[TEvent], None])
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/fa904e10464b6e4f95136eb8c6d988f269e3f1a5/src\events\event_publisher.py#L41)

<a id="src.events.event_publisher.EventPublisher.publish"></a>

#### publish

```python
def publish(event: TEvent)
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/fa904e10464b6e4f95136eb8c6d988f269e3f1a5/src\events\event_publisher.py#L46)

<a id="src.events.event_publisher.EventPublisher.propagate"></a>

#### propagate

```python
def propagate(publisher: 'EventPublisher',
              event_type: Type[TEvent],
              priority: int = EventPriority.NORMAL)
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/fa904e10464b6e4f95136eb8c6d988f269e3f1a5/src\events\event_publisher.py#L56)

For all events publisher publishes of type event_type, publish them to self

<a id="src.events.event_publisher.EventPublisher.propagate_all"></a>

#### propagate\_all

```python
def propagate_all(publisher: 'EventPublisher',
                  priority: int = EventPriority.NORMAL)
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/fa904e10464b6e4f95136eb8c6d988f269e3f1a5/src\events\event_publisher.py#L65)

For all events publisher publishes, publish them to self

