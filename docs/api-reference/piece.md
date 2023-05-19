<a id="chessmaker.chess.base.piece"></a>

# chessmaker.chess.base.piece

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/31277ef9b150ef22d5ea0caafe33d2906b6c7f48/chessmaker\chess\base\piece.py#L1)

<a id="chessmaker.chess.base.piece.AfterGetMoveOptionsEvent"></a>

## AfterGetMoveOptionsEvent

```python
@dataclass(frozen=True)
class AfterGetMoveOptionsEvent(Event)
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/31277ef9b150ef22d5ea0caafe33d2906b6c7f48/chessmaker\chess\base\piece.py#L15)

<a id="chessmaker.chess.base.piece.AfterGetMoveOptionsEvent.piece"></a>

#### piece: `"Piece"`

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/31277ef9b150ef22d5ea0caafe33d2906b6c7f48/chessmaker\chess\base\piece.py#L16)

<a id="chessmaker.chess.base.piece.AfterGetMoveOptionsEvent.move_options"></a>

#### move\_options: `Iterable[MoveOption]`

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/31277ef9b150ef22d5ea0caafe33d2906b6c7f48/chessmaker\chess\base\piece.py#L17)

<a id="chessmaker.chess.base.piece.BeforeGetMoveOptionsEvent"></a>

## BeforeGetMoveOptionsEvent

```python
class BeforeGetMoveOptionsEvent(AfterGetMoveOptionsEvent)
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/31277ef9b150ef22d5ea0caafe33d2906b6c7f48/chessmaker\chess\base\piece.py#L20)

<a id="chessmaker.chess.base.piece.BeforeGetMoveOptionsEvent.set_move_options"></a>

#### set\_move\_options

```python
def set_move_options(move_options: Iterable[MoveOption])
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/31277ef9b150ef22d5ea0caafe33d2906b6c7f48/chessmaker\chess\base\piece.py#L21)

<a id="chessmaker.chess.base.piece.AfterMoveEvent"></a>

## AfterMoveEvent

```python
@dataclass(frozen=True)
class AfterMoveEvent(Event)
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/31277ef9b150ef22d5ea0caafe33d2906b6c7f48/chessmaker\chess\base\piece.py#L26)

<a id="chessmaker.chess.base.piece.AfterMoveEvent.piece"></a>

#### piece: `"Piece"`

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/31277ef9b150ef22d5ea0caafe33d2906b6c7f48/chessmaker\chess\base\piece.py#L27)

<a id="chessmaker.chess.base.piece.AfterMoveEvent.move_option"></a>

#### move\_option: `MoveOption`

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/31277ef9b150ef22d5ea0caafe33d2906b6c7f48/chessmaker\chess\base\piece.py#L28)

<a id="chessmaker.chess.base.piece.BeforeMoveEvent"></a>

## BeforeMoveEvent

```python
class BeforeMoveEvent(AfterMoveEvent,  CancellableEvent)
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/31277ef9b150ef22d5ea0caafe33d2906b6c7f48/chessmaker\chess\base\piece.py#L31)

<a id="chessmaker.chess.base.piece.BeforeMoveEvent.set_move_option"></a>

#### set\_move\_option

```python
def set_move_option(move_option: MoveOption)
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/31277ef9b150ef22d5ea0caafe33d2906b6c7f48/chessmaker\chess\base\piece.py#L32)

<a id="chessmaker.chess.base.piece.AfterCapturedEvent"></a>

## AfterCapturedEvent

```python
@dataclass(frozen=True)
class AfterCapturedEvent(Event)
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/31277ef9b150ef22d5ea0caafe33d2906b6c7f48/chessmaker\chess\base\piece.py#L37)

<a id="chessmaker.chess.base.piece.AfterCapturedEvent.captured_piece"></a>

#### captured\_piece: `"Piece"`

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/31277ef9b150ef22d5ea0caafe33d2906b6c7f48/chessmaker\chess\base\piece.py#L38)

<a id="chessmaker.chess.base.piece.BeforeCapturedEvent"></a>

## BeforeCapturedEvent

```python
class BeforeCapturedEvent(AfterCapturedEvent)
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/31277ef9b150ef22d5ea0caafe33d2906b6c7f48/chessmaker\chess\base\piece.py#L41)

<a id="chessmaker.chess.base.piece.PIECE_EVENT_TYPES"></a>

#### PIECE\_EVENT\_TYPES

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/31277ef9b150ef22d5ea0caafe33d2906b6c7f48/chessmaker\chess\base\piece.py#L45)

<a id="chessmaker.chess.base.piece.Piece"></a>

## Piece

```python
@event_publisher(*PIECE_EVENT_TYPES)
class Piece(Cloneable,  EventPublisher)
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/31277ef9b150ef22d5ea0caafe33d2906b6c7f48/chessmaker\chess\base\piece.py#L50)

<a id="chessmaker.chess.base.piece.Piece.__init__"></a>

#### \_\_init\_\_

```python
def __init__(player: Player)
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/31277ef9b150ef22d5ea0caafe33d2906b6c7f48/chessmaker\chess\base\piece.py#L51)

<a id="chessmaker.chess.base.piece.Piece.__repr__"></a>

#### \_\_repr\_\_

```python
def __repr__()
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/31277ef9b150ef22d5ea0caafe33d2906b6c7f48/chessmaker\chess\base\piece.py#L56)

<a id="chessmaker.chess.base.piece.Piece.get_move_options"></a>

#### get\_move\_options

```python
def get_move_options() -> Iterable[MoveOption]
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/31277ef9b150ef22d5ea0caafe33d2906b6c7f48/chessmaker\chess\base\piece.py#L59)

<a id="chessmaker.chess.base.piece.Piece.move"></a>

#### move

```python
def move(move_option: MoveOption)
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/31277ef9b150ef22d5ea0caafe33d2906b6c7f48/chessmaker\chess\base\piece.py#L69)

<a id="chessmaker.chess.base.piece.Piece.on_join_board"></a>

#### on\_join\_board

```python
def on_join_board()
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/31277ef9b150ef22d5ea0caafe33d2906b6c7f48/chessmaker\chess\base\piece.py#L92)

<a id="chessmaker.chess.base.piece.Piece.position"></a>

#### position

```python
@property
def position()
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/31277ef9b150ef22d5ea0caafe33d2906b6c7f48/chessmaker\chess\base\piece.py#L96)

<a id="chessmaker.chess.base.piece.Piece.board"></a>

#### board

```python
@property
def board()
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/31277ef9b150ef22d5ea0caafe33d2906b6c7f48/chessmaker\chess\base\piece.py#L100)

<a id="chessmaker.chess.base.piece.Piece.name"></a>

#### name

```python
@classmethod
@property
@abstractmethod
def name(cls)
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/31277ef9b150ef22d5ea0caafe33d2906b6c7f48/chessmaker\chess\base\piece.py#L108)

<a id="chessmaker.chess.base.piece.Piece.clone"></a>

#### clone

```python
@abstractmethod
def clone()
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/31277ef9b150ef22d5ea0caafe33d2906b6c7f48/chessmaker\chess\base\piece.py#L116)

