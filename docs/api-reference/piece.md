<a id="chessmaker.chess.base.piece"></a>

# chessmaker.chess.base.piece

<a id="chessmaker.chess.base.piece.AfterGetMoveOptionsEvent"></a>

## AfterGetMoveOptionsEvent

```python
@dataclass(frozen=True)
class AfterGetMoveOptionsEvent(Event)
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/9dc1415fe58befbc9ce03492c419fa5aae04d245/chessmaker\chess\base\piece.py#L14)

<a id="chessmaker.chess.base.piece.AfterGetMoveOptionsEvent.piece"></a>

#### piece: `"Piece"`

<a id="chessmaker.chess.base.piece.AfterGetMoveOptionsEvent.move_options"></a>

#### move\_options: `Iterable[MoveOption]`

<a id="chessmaker.chess.base.piece.BeforeGetMoveOptionsEvent"></a>

## BeforeGetMoveOptionsEvent

```python
class BeforeGetMoveOptionsEvent(AfterGetMoveOptionsEvent)
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/9dc1415fe58befbc9ce03492c419fa5aae04d245/chessmaker\chess\base\piece.py#L18)

<a id="chessmaker.chess.base.piece.BeforeGetMoveOptionsEvent.set_move_options"></a>

#### set\_move\_options

```python
def set_move_options(move_options: Iterable[MoveOption])
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/9dc1415fe58befbc9ce03492c419fa5aae04d245/chessmaker\chess\base\piece.py#L19)

<a id="chessmaker.chess.base.piece.AfterMoveEvent"></a>

## AfterMoveEvent

```python
@dataclass(frozen=True)
class AfterMoveEvent(Event)
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/9dc1415fe58befbc9ce03492c419fa5aae04d245/chessmaker\chess\base\piece.py#L23)

<a id="chessmaker.chess.base.piece.AfterMoveEvent.piece"></a>

#### piece: `"Piece"`

<a id="chessmaker.chess.base.piece.AfterMoveEvent.move_option"></a>

#### move\_option: `MoveOption`

<a id="chessmaker.chess.base.piece.BeforeMoveEvent"></a>

## BeforeMoveEvent

```python
class BeforeMoveEvent(AfterMoveEvent, CancellableEvent)
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/9dc1415fe58befbc9ce03492c419fa5aae04d245/chessmaker\chess\base\piece.py#L27)

<a id="chessmaker.chess.base.piece.BeforeMoveEvent.set_move_option"></a>

#### set\_move\_option

```python
def set_move_option(move_option: MoveOption)
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/9dc1415fe58befbc9ce03492c419fa5aae04d245/chessmaker\chess\base\piece.py#L28)

<a id="chessmaker.chess.base.piece.AfterCaptureEvent"></a>

## AfterCaptureEvent

```python
@dataclass(frozen=True)
class AfterCaptureEvent(Event)
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/9dc1415fe58befbc9ce03492c419fa5aae04d245/chessmaker\chess\base\piece.py#L32)

<a id="chessmaker.chess.base.piece.AfterCaptureEvent.capturing_piece"></a>

#### capturing\_piece: `"Piece"`

<a id="chessmaker.chess.base.piece.AfterCaptureEvent.captured_piece"></a>

#### captured\_piece: `"Piece"`

<a id="chessmaker.chess.base.piece.BeforeCaptureEvent"></a>

## BeforeCaptureEvent

```python
class BeforeCaptureEvent(AfterCaptureEvent)
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/9dc1415fe58befbc9ce03492c419fa5aae04d245/chessmaker\chess\base\piece.py#L36)

<a id="chessmaker.chess.base.piece.PieceEventTypes"></a>

#### PieceEventTypes

<a id="chessmaker.chess.base.piece.Piece"></a>

## Piece

```python
class Piece(EventPublisher[PieceEventTypes], Cloneable)
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/9dc1415fe58befbc9ce03492c419fa5aae04d245/chessmaker\chess\base\piece.py#L43)

<a id="chessmaker.chess.base.piece.Piece.__init__"></a>

#### \_\_init\_\_

```python
def __init__(player: Player)
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/9dc1415fe58befbc9ce03492c419fa5aae04d245/chessmaker\chess\base\piece.py#L44)

<a id="chessmaker.chess.base.piece.Piece.__repr__"></a>

#### \_\_repr\_\_

```python
def __repr__()
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/9dc1415fe58befbc9ce03492c419fa5aae04d245/chessmaker\chess\base\piece.py#L49)

<a id="chessmaker.chess.base.piece.Piece.get_move_options"></a>

#### get\_move\_options

```python
def get_move_options() -> Iterable[MoveOption]
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/9dc1415fe58befbc9ce03492c419fa5aae04d245/chessmaker\chess\base\piece.py#L52)

<a id="chessmaker.chess.base.piece.Piece.move"></a>

#### move

```python
def move(move_option: MoveOption)
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/9dc1415fe58befbc9ce03492c419fa5aae04d245/chessmaker\chess\base\piece.py#L62)

<a id="chessmaker.chess.base.piece.Piece.player"></a>

#### player

```python
@property
def player()
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/9dc1415fe58befbc9ce03492c419fa5aae04d245/chessmaker\chess\base\piece.py#L86)

<a id="chessmaker.chess.base.piece.Piece.position"></a>

#### position

```python
@property
def position()
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/9dc1415fe58befbc9ce03492c419fa5aae04d245/chessmaker\chess\base\piece.py#L90)

<a id="chessmaker.chess.base.piece.Piece.board"></a>

#### board

```python
@property
def board()
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/9dc1415fe58befbc9ce03492c419fa5aae04d245/chessmaker\chess\base\piece.py#L94)

<a id="chessmaker.chess.base.piece.Piece.name"></a>

#### name

```python
@classmethod
@property
@abstractmethod
def name()
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/9dc1415fe58befbc9ce03492c419fa5aae04d245/chessmaker\chess\base\piece.py#L102)

<a id="chessmaker.chess.base.piece.Piece.clone"></a>

#### clone

```python
@abstractmethod
def clone()
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/9dc1415fe58befbc9ce03492c419fa5aae04d245/chessmaker\chess\base\piece.py#L110)

