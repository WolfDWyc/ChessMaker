<a id="src.chess.base.game"></a>

# src.chess.base.game

<a id="src.chess.base.game.AfterGameEndEvent"></a>

## AfterGameEndEvent

```python
@dataclass(frozen=True)
class AfterGameEndEvent(Event)
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/fa904e10464b6e4f95136eb8c6d988f269e3f1a5/src\chess\base\game.py#L10)

<a id="src.chess.base.game.AfterGameEndEvent.game"></a>

#### game: `"Game"`

<a id="src.chess.base.game.AfterGameEndEvent.result"></a>

#### result: `str`

<a id="src.chess.base.game.Game"></a>

## Game

```python
class Game(EventPublisher[AfterGameEndEvent])
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/fa904e10464b6e4f95136eb8c6d988f269e3f1a5/src\chess\base\game.py#L14)

<a id="src.chess.base.game.Game.__init__"></a>

#### \_\_init\_\_

```python
def __init__(board: Board, get_result: Callable[[Board], str | None])
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/fa904e10464b6e4f95136eb8c6d988f269e3f1a5/src\chess\base\game.py#L15)

