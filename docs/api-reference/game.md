<a id="chessmaker.chess.base.game"></a>

# chessmaker.chess.base.game

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/31277ef9b150ef22d5ea0caafe33d2906b6c7f48/chessmaker\chess\base\game.py#L1)

<a id="chessmaker.chess.base.game.AfterGameEndEvent"></a>

## AfterGameEndEvent

```python
@dataclass(frozen=True)
class AfterGameEndEvent(Event)
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/31277ef9b150ef22d5ea0caafe33d2906b6c7f48/chessmaker\chess\base\game.py#L9)

<a id="chessmaker.chess.base.game.AfterGameEndEvent.game"></a>

#### game: `"Game"`

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/31277ef9b150ef22d5ea0caafe33d2906b6c7f48/chessmaker\chess\base\game.py#L10)

<a id="chessmaker.chess.base.game.AfterGameEndEvent.result"></a>

#### result: `str`

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/31277ef9b150ef22d5ea0caafe33d2906b6c7f48/chessmaker\chess\base\game.py#L11)

<a id="chessmaker.chess.base.game.Game"></a>

## Game

```python
@event_publisher(AfterGameEndEvent)
class Game(EventPublisher)
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/31277ef9b150ef22d5ea0caafe33d2906b6c7f48/chessmaker\chess\base\game.py#L15)

<a id="chessmaker.chess.base.game.Game.__init__"></a>

#### \_\_init\_\_

```python
def __init__(board: Board, get_result: Callable[[Board], str | None])
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/31277ef9b150ef22d5ea0caafe33d2906b6c7f48/chessmaker\chess\base\game.py#L16)

