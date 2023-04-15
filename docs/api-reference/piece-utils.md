<a id="chessmaker.chess.piece_utils"></a>

# chessmaker.chess.piece\_utils

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/ebfedfed6255bde50e4271e927362d114af5a744/chessmaker\chess\piece_utils.py#L1)

<a id="chessmaker.chess.piece_utils.is_in_board"></a>

#### is\_in\_board

```python
def is_in_board(board: Board, position: Position) -> bool
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/ebfedfed6255bde50e4271e927362d114af5a744/chessmaker\chess\piece_utils.py#L9)

<a id="chessmaker.chess.piece_utils.iterate_until_blocked"></a>

#### iterate\_until\_blocked

```python
def iterate_until_blocked(piece: Piece, direction: tuple[int, int]) -> Iterable[Position]
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/ebfedfed6255bde50e4271e927362d114af5a744/chessmaker\chess\piece_utils.py#L20)

<a id="chessmaker.chess.piece_utils.get_diagonals_until_blocked"></a>

#### get\_diagonals\_until\_blocked

```python
def get_diagonals_until_blocked(piece: Piece) -> Iterable[Position]
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/ebfedfed6255bde50e4271e927362d114af5a744/chessmaker\chess\piece_utils.py#L39)

<a id="chessmaker.chess.piece_utils.get_horizontal_until_blocked"></a>

#### get\_horizontal\_until\_blocked

```python
def get_horizontal_until_blocked(piece: Piece) -> Iterable[Position]
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/ebfedfed6255bde50e4271e927362d114af5a744/chessmaker\chess\piece_utils.py#L44)

<a id="chessmaker.chess.piece_utils.get_vertical_until_blocked"></a>

#### get\_vertical\_until\_blocked

```python
def get_vertical_until_blocked(piece: Piece) -> Iterable[Position]
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/ebfedfed6255bde50e4271e927362d114af5a744/chessmaker\chess\piece_utils.py#L49)

<a id="chessmaker.chess.piece_utils.get_straight_until_blocked"></a>

#### get\_straight\_until\_blocked

```python
def get_straight_until_blocked(piece: Piece) -> Iterable[Position]
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/ebfedfed6255bde50e4271e927362d114af5a744/chessmaker\chess\piece_utils.py#L54)

<a id="chessmaker.chess.piece_utils.filter_uncapturable_positions"></a>

#### filter\_uncapturable\_positions

```python
def filter_uncapturable_positions(piece: Piece, positions: Iterable[Position]) -> Iterable[Position]
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/ebfedfed6255bde50e4271e927362d114af5a744/chessmaker\chess\piece_utils.py#L59)

<a id="chessmaker.chess.piece_utils.positions_to_move_options"></a>

#### positions\_to\_move\_options

```python
def positions_to_move_options(board: Board, positions: Iterable[Position]) -> Iterable[MoveOption]
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/ebfedfed6255bde50e4271e927362d114af5a744/chessmaker\chess\piece_utils.py#L70)

