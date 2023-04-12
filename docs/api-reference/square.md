<a id="src.chess.base.square"></a>

# src.chess.base.square

<a id="src.chess.base.square.AfterAddPieceEvent"></a>

## AfterAddPieceEvent

```python
@dataclass(frozen=True)
class AfterAddPieceEvent(Event)
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/fa904e10464b6e4f95136eb8c6d988f269e3f1a5/src\chess\base\square.py#L13)

<a id="src.chess.base.square.AfterAddPieceEvent.square"></a>

#### square: `"Square"`

<a id="src.chess.base.square.AfterAddPieceEvent.piece"></a>

#### piece: `Piece`

<a id="src.chess.base.square.BeforeAddPieceEvent"></a>

## BeforeAddPieceEvent

```python
class BeforeAddPieceEvent(AfterAddPieceEvent)
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/fa904e10464b6e4f95136eb8c6d988f269e3f1a5/src\chess\base\square.py#L17)

<a id="src.chess.base.square.BeforeAddPieceEvent.set_piece"></a>

#### set\_piece

```python
def set_piece(piece: Piece)
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/fa904e10464b6e4f95136eb8c6d988f269e3f1a5/src\chess\base\square.py#L18)

<a id="src.chess.base.square.BeforeRemovePieceEvent"></a>

## BeforeRemovePieceEvent

```python
@dataclass(frozen=True)
class BeforeRemovePieceEvent(Event)
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/fa904e10464b6e4f95136eb8c6d988f269e3f1a5/src\chess\base\square.py#L22)

<a id="src.chess.base.square.BeforeRemovePieceEvent.square"></a>

#### square: `"Square"`

<a id="src.chess.base.square.BeforeRemovePieceEvent.piece"></a>

#### piece: `Piece`

<a id="src.chess.base.square.AfterRemovePieceEvent"></a>

## AfterRemovePieceEvent

```python
class AfterRemovePieceEvent(BeforeRemovePieceEvent)
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/fa904e10464b6e4f95136eb8c6d988f269e3f1a5/src\chess\base\square.py#L26)

<a id="src.chess.base.square.Square"></a>

## Square

```python
class Square(EventPublisher[BeforeAddPieceEvent | AfterAddPieceEvent
                            | BeforeRemovePieceEvent | AfterRemovePieceEvent],
             Cloneable)
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/fa904e10464b6e4f95136eb8c6d988f269e3f1a5/src\chess\base\square.py#L30)

<a id="src.chess.base.square.Square.__init__"></a>

#### \_\_init\_\_

```python
def __init__(piece: Piece | None = None)
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/fa904e10464b6e4f95136eb8c6d988f269e3f1a5/src\chess\base\square.py#L31)

<a id="src.chess.base.square.Square.piece"></a>

#### piece

```python
@property
def piece() -> Piece
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/fa904e10464b6e4f95136eb8c6d988f269e3f1a5/src\chess\base\square.py#L37)

<a id="src.chess.base.square.Square.position"></a>

#### position

```python
@property
def position()
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/fa904e10464b6e4f95136eb8c6d988f269e3f1a5/src\chess\base\square.py#L41)

<a id="src.chess.base.square.Square.piece"></a>

#### piece

```python
@piece.setter
def piece(piece: Piece)
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/fa904e10464b6e4f95136eb8c6d988f269e3f1a5/src\chess\base\square.py#L45)

<a id="src.chess.base.square.Square.clone"></a>

#### clone

```python
def clone()
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/fa904e10464b6e4f95136eb8c6d988f269e3f1a5/src\chess\base\square.py#L66)

