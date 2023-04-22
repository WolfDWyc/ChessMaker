<a id="chessmaker.chess.base.square"></a>

# chessmaker.chess.base.square

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/eb72eddc40bfcf661740274ff3857c0e0abd22f6/chessmaker\chess\base\square.py#L1)

<a id="chessmaker.chess.base.square.AfterAddPieceEvent"></a>

## AfterAddPieceEvent

```python
@dataclass(frozen=True)
class AfterAddPieceEvent(Event)
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/eb72eddc40bfcf661740274ff3857c0e0abd22f6/chessmaker\chess\base\square.py#L14)

<a id="chessmaker.chess.base.square.AfterAddPieceEvent.square"></a>

#### square: `"Square"`

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/eb72eddc40bfcf661740274ff3857c0e0abd22f6/chessmaker\chess\base\square.py#L15)

<a id="chessmaker.chess.base.square.AfterAddPieceEvent.piece"></a>

#### piece: `"Piece"`

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/eb72eddc40bfcf661740274ff3857c0e0abd22f6/chessmaker\chess\base\square.py#L16)

<a id="chessmaker.chess.base.square.BeforeAddPieceEvent"></a>

## BeforeAddPieceEvent

```python
class BeforeAddPieceEvent(AfterAddPieceEvent)
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/eb72eddc40bfcf661740274ff3857c0e0abd22f6/chessmaker\chess\base\square.py#L19)

<a id="chessmaker.chess.base.square.BeforeAddPieceEvent.set_piece"></a>

#### set\_piece

```python
def set_piece(piece: "Piece")
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/eb72eddc40bfcf661740274ff3857c0e0abd22f6/chessmaker\chess\base\square.py#L20)

<a id="chessmaker.chess.base.square.BeforeRemovePieceEvent"></a>

## BeforeRemovePieceEvent

```python
@dataclass(frozen=True)
class BeforeRemovePieceEvent(Event)
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/eb72eddc40bfcf661740274ff3857c0e0abd22f6/chessmaker\chess\base\square.py#L25)

<a id="chessmaker.chess.base.square.BeforeRemovePieceEvent.square"></a>

#### square: `"Square"`

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/eb72eddc40bfcf661740274ff3857c0e0abd22f6/chessmaker\chess\base\square.py#L26)

<a id="chessmaker.chess.base.square.BeforeRemovePieceEvent.piece"></a>

#### piece: `"Piece"`

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/eb72eddc40bfcf661740274ff3857c0e0abd22f6/chessmaker\chess\base\square.py#L27)

<a id="chessmaker.chess.base.square.AfterRemovePieceEvent"></a>

## AfterRemovePieceEvent

```python
class AfterRemovePieceEvent(BeforeRemovePieceEvent)
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/eb72eddc40bfcf661740274ff3857c0e0abd22f6/chessmaker\chess\base\square.py#L30)

<a id="chessmaker.chess.base.square.SQUARE_EVENT_TYPES"></a>

#### SQUARE\_EVENT\_TYPES

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/eb72eddc40bfcf661740274ff3857c0e0abd22f6/chessmaker\chess\base\square.py#L34)

<a id="chessmaker.chess.base.square.Square"></a>

## Square

```python
@event_publisher(*SQUARE_EVENT_TYPES)
class Square(Cloneable,  EventPublisher)
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/eb72eddc40bfcf661740274ff3857c0e0abd22f6/chessmaker\chess\base\square.py#L38)

<a id="chessmaker.chess.base.square.Square.__init__"></a>

#### \_\_init\_\_

```python
def __init__(piece: Optional["Piece"] = None)
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/eb72eddc40bfcf661740274ff3857c0e0abd22f6/chessmaker\chess\base\square.py#L39)

<a id="chessmaker.chess.base.square.Square.piece"></a>

#### piece

```python
@property
def piece() -> "Piece"
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/eb72eddc40bfcf661740274ff3857c0e0abd22f6/chessmaker\chess\base\square.py#L45)

<a id="chessmaker.chess.base.square.Square.position"></a>

#### position

```python
@property
def position()
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/eb72eddc40bfcf661740274ff3857c0e0abd22f6/chessmaker\chess\base\square.py#L49)

<a id="chessmaker.chess.base.square.Square.board"></a>

#### board

```python
@property
def board()
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/eb72eddc40bfcf661740274ff3857c0e0abd22f6/chessmaker\chess\base\square.py#L53)

<a id="chessmaker.chess.base.square.Square.piece"></a>

#### piece

```python
@piece.setter
def piece(piece: "Piece")
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/eb72eddc40bfcf661740274ff3857c0e0abd22f6/chessmaker\chess\base\square.py#L59)

<a id="chessmaker.chess.base.square.Square.clone"></a>

#### clone

```python
def clone()
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/eb72eddc40bfcf661740274ff3857c0e0abd22f6/chessmaker\chess\base\square.py#L80)

