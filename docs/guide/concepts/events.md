# Events

## Introduction

ChessMaker uses a custom event system to allow altering and extending the game logic. 
This allows you to add custom logic to the game without having to modify the engine code.

The event system is inspired by [Spigot's Event API](https://www.spigotmc.org/wiki/using-the-event-api/).

## Events
The event system defines a base `Event` dataclass that all event types inherit from.
All attributes of the event are immutable by default, and the event exposes
one function called _set, which allows event types to make a specific attribute mutable.

Generally, things that happen expose a **before** and **after** event,
with some only exposing an **after** event. A common pattern is for **after** events
to be completely immutable, and for **before** events to have mutable attributes.

```python
from dataclasses import dataclass
from chessmaker.events import Event
from chessmaker.chess.base.move_option import MoveOption

# An immutable event
@dataclass(frozen=True)
class AfterMoveEvent(Event):
    piece: "Piece"
    move_option: MoveOption

# A mutable event
class BeforeMoveEvent(AfterMoveEvent):
    def set_move_option(self, move_option: MoveOption):
        self._set("move_option", move_option)
```

### Cancellable Events
Events can also inherit from the `CancellableEvent` class, 
which adds a `cancelled` attribute and a `set_cancelled` function to the event.

```python
from chessmaker.events import CancellableEvent

class BeforeMoveEvent(AfterMoveEvent, CancellableEvent):
    def set_move_option(self, move_option: MoveOption):
        self._set("move_option", move_option)
```


!!! note
    Most of the time, you're going to be subscribing to existing events,
    but if you are creating a new event, you should remember events are just dataclasses - and don't actually
    implement logic like cancelling or mutating. 
    It is the publisher's responsibility to use the mutated event in the correct way.


## Subscribing to events
To subscribe to events, you need to subscribe to a publisher with the event type and callback function.
Events are subscribed to on a per-instance basis - when you subscribe to a Pawn moving,
it will only subscribe to that specific pawn - not all pawns.

```python
import random

board: Board = ...

def on_after_turn_change(event: BeforeTurnChangeEvent):
    if random.random() < 0.5:
        event.set_cancelled(True)
    else:
        event.set_next_player(event.board.players[1])
        
    

board.subscribe(BeforeTurnChangeEvent, on_after_turn_change)
```

!!! tip
    In you event's callback function, you should use the arguments from the event,
    rather than using ones from your outer scope (For example, `board` in the above example).
    This is related to Cloneables, and will be explained later.

### Event Priorities
Events can be subscribed to with a priority, which determines the order in which they are called -
a higher priority means the event is called earlier.

For most use cases, the default priority of `0` is fine,
but if you need to ensure your event is called before or after another event,
you can either use the `EventPriority` enum to specify a priority, or use an integer for more fine-grained control.

```python
from chessmaker.events import EventPriority

board.subscribe(BeforeTurnChangeEvent, on_after_turn_change)
board.subscribe(BeforeTurnChangeEvent, on_after_turn_change, priority=EventPriority.VERY_LOW)
board.subscribe(BeforeTurnChangeEvent, on_after_turn_change, 2000)
```


### Subscribing to all events of an instance
You can also subscribe to all events of an instance by using the `subscribe_all` function.

```python

def on_any_event(_: Event):
    print("Something happened to the board!")
    
board.subscribe_all(on_any_event)
```

### Unsubscribing from events

To unsubscribe from events, you need to call the `unsubscribe` function with the same arguments you used to subscribe.
Similarly, you can use `unsubscribe_all` to unsubscribe from all events of an instance.

```python
board.unsubscribe(BeforeTurnChangeEvent, on_after_turn_change)
board.unsubscribe_all(on_any_event)
```

## Publishing events

If you're adding new code, and want to make that code extendable - it is recommended to publish events.
For an instance to publish events, it needs to inherit from the `EventPublisher` class.

For typing purposes, it is recommended to specify which event types your publisher publishes
using generics and unions.

```python

from chessmaker.events import EventPublisher

class MyPrinter(EventPublisher[BeforePrintEvent | AfterPrintEvent]):
    
    def print_number(self):
        number = str(random.randint(0, 100))
        before_print_event = BeforePrintEvent(self, number)
        self.publish(before_print_event)
        if not before_print_event.cancelled:
            print(before_print_event.number)
            self.publish(AfterPrintEvent(self, number))
```

### Propagating events
Sometimes, you may want to publish events from a publisher to another one.
You can do this either to all event types, or to a specific one.

```python

class MyPrinterManager(EventPublisher[BeforePrintEvent | AfterPrintEvent]):
    
    def __init__(self, my_printer: MyPrinter):
        self.my_printer = my_printer
        self.my_printer.propagate_all(self)
        self.my_printer.propagate(BeforePrintEvent, self)
```

Now, every time the printer publishes an event, the manager will also publish it.
Currently, you can not unpropagate events.

!!! info
    The main use of this in the game is the board propagating all events of its pieces and squares to itself.
    This means that instead of subscribing to a specific piece move, you can subscribe to all pieces moving by subscribing to the board.









