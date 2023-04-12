<a id="chessmaker.chess.base.game"></a>

# chessmaker.chess.base.game

<a id="chessmaker.chess.base.game.AfterGameEndEvent"></a>

## AfterGameEndEvent

```python
@dataclass(frozen=True)
class AfterGameEndEvent(Event)
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/dc56d4841f94820eba4c40c003f75d8396c128d9/chessmaker\chess\base\game.py#L10)

<a id="chessmaker.chess.base.game.AfterGameEndEvent.game"></a>

#### game: `"Game"`

<a id="chessmaker.chess.base.game.AfterGameEndEvent.result"></a>

#### result: `str`

<a id="chessmaker.chess.base.game.Game"></a>

## Game

```python
class Game(EventPublisher[AfterGameEndEvent])
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/dc56d4841f94820eba4c40c003f75d8396c128d9/chessmaker\chess\base\game.py#L14)

<a id="chessmaker.chess.base.game.Game.__init__"></a>

#### \_\_init\_\_

```python
def __init__(board: Board, get_result: Callable[[Board], str | None])
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/dc56d4841f94820eba4c40c003f75d8396c128d9/chessmaker\chess\base\game.py#L15)

