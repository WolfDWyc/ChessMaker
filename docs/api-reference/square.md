<a id="chessmaker.chess.base.square"></a>

# chessmaker.chess.base.square

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/ebfedfed6255bde50e4271e927362d114af5a744/chessmaker\chess\base\square.py#L1)

<a id="chessmaker.chess.base.square.AfterAddPieceEvent"></a>

## AfterAddPieceEvent

```python
@dataclass(frozen=True)
class AfterAddPieceEvent(Event)
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/ebfedfed6255bde50e4271e927362d114af5a744/chessmaker\chess\base\square.py#L13)

<a id="chessmaker.chess.base.square.AfterAddPieceEvent.square"></a>

#### square: `"Square"`

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/ebfedfed6255bde50e4271e927362d114af5a744/chessmaker\chess\base\square.py#L14)

<a id="chessmaker.chess.base.square.AfterAddPieceEvent.piece"></a>

#### piece: `Piece`

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/ebfedfed6255bde50e4271e927362d114af5a744/chessmaker\chess\base\square.py#L15)

<a id="chessmaker.chess.base.square.BeforeAddPieceEvent"></a>

## BeforeAddPieceEvent

```python
class BeforeAddPieceEvent(AfterAddPieceEvent)
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/ebfedfed6255bde50e4271e927362d114af5a744/chessmaker\chess\base\square.py#L17)

<a id="chessmaker.chess.base.square.BeforeAddPieceEvent.set_piece"></a>

#### set\_piece

```python
def set_piece(piece: Piece)
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/ebfedfed6255bde50e4271e927362d114af5a744/chessmaker\chess\base\square.py#L18)

<a id="chessmaker.chess.base.square.BeforeRemovePieceEvent"></a>

## BeforeRemovePieceEvent

```python
@dataclass(frozen=True)
class BeforeRemovePieceEvent(Event)
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/ebfedfed6255bde50e4271e927362d114af5a744/chessmaker\chess\base\square.py#L22)

<a id="chessmaker.chess.base.square.BeforeRemovePieceEvent.square"></a>

#### square: `"Square"`

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/ebfedfed6255bde50e4271e927362d114af5a744/chessmaker\chess\base\square.py#L23)

<a id="chessmaker.chess.base.square.BeforeRemovePieceEvent.piece"></a>

#### piece: `Piece`

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/ebfedfed6255bde50e4271e927362d114af5a744/chessmaker\chess\base\square.py#L24)

<a id="chessmaker.chess.base.square.AfterRemovePieceEvent"></a>

## AfterRemovePieceEvent

```python
class AfterRemovePieceEvent(BeforeRemovePieceEvent)
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/ebfedfed6255bde50e4271e927362d114af5a744/chessmaker\chess\base\square.py#L26)

<a id="chessmaker.chess.base.square.Square"></a>

## Square

```python
class Square(EventPublisher[BeforeAddPieceEvent | AfterAddPieceEvent | BeforeRemovePieceEvent | AfterRemovePieceEvent],  Cloneable)
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/ebfedfed6255bde50e4271e927362d114af5a744/chessmaker\chess\base\square.py#L30)

<a id="chessmaker.chess.base.square.Square.__init__"></a>

#### \_\_init\_\_

```python
def __init__(piece: Piece | None = None)
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/ebfedfed6255bde50e4271e927362d114af5a744/chessmaker\chess\base\square.py#L31)

<a id="chessmaker.chess.base.square.Square.piece"></a>

#### piece

```python
@property
def piece() -> Piece
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/ebfedfed6255bde50e4271e927362d114af5a744/chessmaker\chess\base\square.py#L37)

<a id="chessmaker.chess.base.square.Square.position"></a>

#### position

```python
@property
def position()
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/ebfedfed6255bde50e4271e927362d114af5a744/chessmaker\chess\base\square.py#L41)

<a id="chessmaker.chess.base.square.Square.board"></a>

#### board

```python
@property
def board()
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/ebfedfed6255bde50e4271e927362d114af5a744/chessmaker\chess\base\square.py#L45)

<a id="chessmaker.chess.base.square.Square.piece"></a>

#### piece

```python
@piece.setter
def piece(piece: Piece)
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/ebfedfed6255bde50e4271e927362d114af5a744/chessmaker\chess\base\square.py#L51)

<a id="chessmaker.chess.base.square.Square.clone"></a>

#### clone

```python
def clone()
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/ebfedfed6255bde50e4271e927362d114af5a744/chessmaker\chess\base\square.py#L72)

