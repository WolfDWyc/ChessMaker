<a id="chessmaker.chess.base.game"></a>

# chessmaker.chess.base.game

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/ebfedfed6255bde50e4271e927362d114af5a744/chessmaker\chess\base\game.py#L1)

<a id="chessmaker.chess.base.game.AfterGameEndEvent"></a>

## AfterGameEndEvent

```python
@dataclass(frozen=True)
class AfterGameEndEvent(Event)
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/ebfedfed6255bde50e4271e927362d114af5a744/chessmaker\chess\base\game.py#L10)

<a id="chessmaker.chess.base.game.AfterGameEndEvent.game"></a>

#### game: `"Game"`

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/ebfedfed6255bde50e4271e927362d114af5a744/chessmaker\chess\base\game.py#L11)

<a id="chessmaker.chess.base.game.AfterGameEndEvent.result"></a>

#### result: `str`

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/ebfedfed6255bde50e4271e927362d114af5a744/chessmaker\chess\base\game.py#L12)

<a id="chessmaker.chess.base.game.Game"></a>

## Game

```python
class Game(EventPublisher[AfterGameEndEvent])
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/ebfedfed6255bde50e4271e927362d114af5a744/chessmaker\chess\base\game.py#L14)

<a id="chessmaker.chess.base.game.Game.__init__"></a>

#### \_\_init\_\_

```python
def __init__(board: Board, get_result: Callable[[Board], str | None])
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/ebfedfed6255bde50e4271e927362d114af5a744/chessmaker\chess\base\game.py#L15)

