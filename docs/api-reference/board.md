<a id="src.chess.base.board"></a>

# src.chess.base.board

<a id="src.chess.base.board.AfterNewPieceEvent"></a>

## AfterNewPieceEvent

```python
@dataclass(frozen=True)
class AfterNewPieceEvent(Event)
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/fa904e10464b6e4f95136eb8c6d988f269e3f1a5/src\chess\base\board.py#L17)

<a id="src.chess.base.board.AfterNewPieceEvent.piece"></a>

#### piece: `Piece`

<a id="src.chess.base.board.AfterRemoveSquareEvent"></a>

## AfterRemoveSquareEvent

```python
@dataclass(frozen=True)
class AfterRemoveSquareEvent(Event)
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/fa904e10464b6e4f95136eb8c6d988f269e3f1a5/src\chess\base\board.py#L21)

<a id="src.chess.base.board.AfterRemoveSquareEvent.position"></a>

#### position: `Position`

<a id="src.chess.base.board.AfterRemoveSquareEvent.square"></a>

#### square: `Square`

<a id="src.chess.base.board.BeforeRemoveSquareEvent"></a>

## BeforeRemoveSquareEvent

```python
@dataclass(frozen=True)
class BeforeRemoveSquareEvent(AfterRemoveSquareEvent)
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/fa904e10464b6e4f95136eb8c6d988f269e3f1a5/src\chess\base\board.py#L26)

<a id="src.chess.base.board.AfterAddSquareEvent"></a>

## AfterAddSquareEvent

```python
@dataclass(frozen=True)
class AfterAddSquareEvent(Event)
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/fa904e10464b6e4f95136eb8c6d988f269e3f1a5/src\chess\base\board.py#L30)

<a id="src.chess.base.board.AfterAddSquareEvent.position"></a>

#### position: `Position`

<a id="src.chess.base.board.AfterAddSquareEvent.square"></a>

#### square: `Square`

<a id="src.chess.base.board.BeforeAddSquareEvent"></a>

## BeforeAddSquareEvent

```python
@dataclass(frozen=True)
class BeforeAddSquareEvent(AfterAddSquareEvent)
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/fa904e10464b6e4f95136eb8c6d988f269e3f1a5/src\chess\base\board.py#L35)

<a id="src.chess.base.board.BeforeAddSquareEvent.set_square"></a>

#### set\_square

```python
def set_square(square: Square)
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/fa904e10464b6e4f95136eb8c6d988f269e3f1a5/src\chess\base\board.py#L36)

<a id="src.chess.base.board.BeforeTurnChangeEvent"></a>

## BeforeTurnChangeEvent

```python
@dataclass(frozen=True)
class BeforeTurnChangeEvent(CancellableEvent)
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/fa904e10464b6e4f95136eb8c6d988f269e3f1a5/src\chess\base\board.py#L40)

<a id="src.chess.base.board.BeforeTurnChangeEvent.board"></a>

#### board: `"Board"`

<a id="src.chess.base.board.BeforeTurnChangeEvent.next_player"></a>

#### next\_player: `Player`

<a id="src.chess.base.board.BeforeTurnChangeEvent.set_next_player"></a>

#### set\_next\_player

```python
def set_next_player(next_player: Player)
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/fa904e10464b6e4f95136eb8c6d988f269e3f1a5/src\chess\base\board.py#L44)

<a id="src.chess.base.board.AfterTurnChangeEvent"></a>

## AfterTurnChangeEvent

```python
@dataclass(frozen=True)
class AfterTurnChangeEvent(Event)
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/fa904e10464b6e4f95136eb8c6d988f269e3f1a5/src\chess\base\board.py#L48)

<a id="src.chess.base.board.AfterTurnChangeEvent.board"></a>

#### board: `"Board"`

<a id="src.chess.base.board.AfterTurnChangeEvent.player"></a>

#### player: `Player`

<a id="src.chess.base.board.Board"></a>

## Board

```python
class Board(EventPublisher[BeforeAddPieceEvent | AfterAddPieceEvent
                           | BeforeRemovePieceEvent | AfterRemovePieceEvent
                           | PieceEventTypes | AfterNewPieceEvent
                           | BeforeAddSquareEvent | AfterAddSquareEvent
                           | BeforeRemoveSquareEvent | AfterRemoveSquareEvent
                           | BeforeTurnChangeEvent
                           | AfterTurnChangeEvent], Cloneable)
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/fa904e10464b6e4f95136eb8c6d988f269e3f1a5/src\chess\base\board.py#L52)

<a id="src.chess.base.board.Board.__init__"></a>

#### \_\_init\_\_

```python
def __init__(squares: list[list[Square | None]],
             players: list[Player],
             turn_iterator: Iterator[Player],
             rules: list[Rule] = None)
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/fa904e10464b6e4f95136eb8c6d988f269e3f1a5/src\chess\base\board.py#L56)

<a id="src.chess.base.board.Board.__getitem__"></a>

#### \_\_getitem\_\_

```python
def __getitem__(position: Position) -> Square | None
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/fa904e10464b6e4f95136eb8c6d988f269e3f1a5/src\chess\base\board.py#L107)

<a id="src.chess.base.board.Board.__setitem__"></a>

#### \_\_setitem\_\_

```python
def __setitem__(position: Position, square: Square | None)
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/fa904e10464b6e4f95136eb8c6d988f269e3f1a5/src\chess\base\board.py#L110)

<a id="src.chess.base.board.Board.__iter__"></a>

#### \_\_iter\_\_

```python
def __iter__() -> Iterable[Square]
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/fa904e10464b6e4f95136eb8c6d988f269e3f1a5/src\chess\base\board.py#L133)

<a id="src.chess.base.board.Board.get_pieces"></a>

#### get\_pieces

```python
def get_pieces() -> Iterable[Piece]
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/fa904e10464b6e4f95136eb8c6d988f269e3f1a5/src\chess\base\board.py#L152)

<a id="src.chess.base.board.Board.get_player_pieces"></a>

#### get\_player\_pieces

```python
def get_player_pieces(player: Player) -> Iterable[Piece]
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/fa904e10464b6e4f95136eb8c6d988f269e3f1a5/src\chess\base\board.py#L157)

<a id="src.chess.base.board.Board.clone"></a>

#### clone

```python
def clone()
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/fa904e10464b6e4f95136eb8c6d988f269e3f1a5/src\chess\base\board.py#L162)

