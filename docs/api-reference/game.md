<a id="chessmaker.chess.base.game"></a>

# chessmaker.chess.base.game

<a id="chessmaker.chess.base.game.AfterGameEndEvent"></a>

## AfterGameEndEvent

```python
@dataclass(frozen=True)
class AfterGameEndEvent(Event)
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/9dc1415fe58befbc9ce03492c419fa5aae04d245/chessmaker\chess\base\game.py#L10)

<a id="chessmaker.chess.base.game.AfterGameEndEvent.game"></a>

#### game: `"Game"`

<a id="chessmaker.chess.base.game.AfterGameEndEvent.result"></a>

#### result: `str`

<a id="chessmaker.chess.base.game.Game"></a>

## Game

```python
class Game(EventPublisher[AfterGameEndEvent])
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/9dc1415fe58befbc9ce03492c419fa5aae04d245/chessmaker\chess\base\game.py#L14)

<a id="chessmaker.chess.base.game.Game.__init__"></a>

#### \_\_init\_\_

```python
def __init__(board: Board, get_result: Callable[[Board], str | None])
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/9dc1415fe58befbc9ce03492c419fa5aae04d245/chessmaker\chess\base\game.py#L15)

