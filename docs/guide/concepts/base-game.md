# Base Game

In this section we'll look at everything a game has to have.

This section contains an overview of each concept, and tries to highlight useful methods,
but it's not a complete reference - for that, you should look at the API Reference.

## Game

The game class is a container for the board and the result function.
It doesn't do much except for having an `AfterGameEndEvent` event that is published when the game ends.

```python
game = Game(board, get_result)
game.subscribe(AfterGameEndEvent, lambda event: print(event.result))
```

## Result

The result function is a function that is called after every turn - it takes a board and returns either None or a string.
There is no structure to the string - and it's used to tell the client what the result of the game is,
but if the string returned is not None, the game will end.

For a result function to have state (e.g. 50 move rule) it should be wrapped in a class that has a `__call__` method.

```python

class GetDumbResult:
    def __init__(self):
        self.move_count = 0
        
    def __call__(self, board: Board) -> Optional[str]:
        self.move_count += 1
        if self.move_count > 100:
            return "Draw - I'm bored"
        return None
```

## Board

The board is the main container for all squares.
It also contains the players and the turn iterator.

It's important to understand is that even though the board contains a turn iterator,
it (or the Game itself) doesn't actually manage a game loop - it leaves that to any client.

A board contains a 2D list of squares - these squares can be Non (e.g. holes) 
to create non-rectangular boards. When a square in the board changes (Not to confuse with when a piece changes)
the board can publish `BeforeRemoveSquareEvent`, `AfterRemoveSquareEvent`, `BeforeAddSquareEvent` and `AfterAddSquareEvent`.

The board also contains a list of players, and a turn iterator.
The turn iterator is a generator that will be called to get the next player in the turn order.
When this happens, the board publishes a `BeforeChangeTurnEvent` and `AfterChangeTurnEvent`.

The board propogates all events from the squares and pieces it contains,
which is very useful for subscribing to all of them at once.
and also publishes `AfterNewPieceEvent` when a new piece is added to the board.

It also contains a lot of utility methods for getting squares, pieces and players.

```python
board = Board(squares, players, turn_iterator)

# Get a square
square = board[0][0]
piece = square.piece

for square in board:
    print(square.position)
    
for y in board.size[1]:
    for x in board.size[0]:
        print(Position(x, y))
        
for player_piece in board.get_player_pieces(piece.player):
    print(player_piece)
```


## Player

The player class is a simple container that is used to identify the owner of a piece.
The name chosen is arbitrary - and doesn't have to be unique.

```python
player0 = Player()
player1 = Player("white")
player2 = Player("my_player2")
```

## Position

A position is a named tuple that contains the x and y coordinates of a square or piece.
`Position(0, 0)` is at the top left of the board.

```
position = Position(0, 0)
print(position)
print(position.x, position.y)
print(position[0], position[1])

print(position.offset(1, 1))
```

!!! tip
    While both pieces and squares have a `position` attribute, it doesn't need to be changed manually.
    instead the board knows where each piece and square is, and the `position` attribute
    simply asks the board for its position.

## Square

A square is a container for a piece. When setting a square's piece,
it can publish `BeforeRemovePieceEvent`, `AfterRemovePieceEvent`, `BeforeAddPieceEvent` and `AfterAddPieceEvent`.

The square has an (auto-updating) `position` attribute, and a `piece` attribute.

```python

board = ...
square = board[0][0]
print(square.position, square.piece)

square.subscribe(AfterAddPieceEvent, lambda event: print(event.piece))

square.piece = Pawn(player0)
```

## Piece
The piece is the main class in the base game that is meant to be extended.
The piece is an abstract class, and must be extended to be used.

A piece has an (immutable) `player` attribute, and an (auto-updating) `position` attribute.
It also has a `name` class attribute, which is used for display purposes.

The piece also has a `board` attribute, which is set when the piece is added to a board.
Because the piece is created before it's added to the board, trying to access it when it's created will result in an
error saying `Piece is not on the board yet`. A common practice on how to do this properly 
for the piece to subscribe to the `AfterNewPieceEvent` event of itself in it's `__init__` method.

Each piece has to implement a `_get_move_options` method, which returns an iterable of what moves the piece can make.
Then, when the piece is asked for its move options, it will call the `_get_move_options` method and publish
`BeforeGetMoveOptionsEvent` and `AfterGetMoveOptionsEvent` events.

Then, a move option is selected by the player, and the piece is asked to make the move using `.move()` - which
will publish `BeforeMoveEvent`, `AfterMoveEvent`, `BeforeCaptureEvent` and `AfterCaptureEvent` events.

For a piece to implement moves that are more complex than just moving and capturing,
it should subscribe to it's own `BeforeMoveEvent` and `AfterMoveEvent` events, and implement the logic there.

### Move Option
A MoveOption is used to describe a move that a piece can make.
A move option has to specify the `position` it will move to with the `position` attribute,
and all positions it will capture with the `captures` attribute.

In addition, for special moves (e.g. castling, en passant) a move option can have an `extra` attribute,
which is a dict. Ideally, this dict shouldn't contain complex objects like pieces or other dicts, but instead
positions or other simple objects.

```python
class CoolPiece(Piece):
    """
    A piece that can move one square diagonally (down and right).
    """

    @classmethod
    @property
    def name(cls):
        return "CoolPiece"

    def _get_move_options(self) -> Iterable[MoveOption]:
        move_position = self.position.offset(1, 1)

        if not is_in_board(self.board, move_position):
            return

        if (self.board[move_position].piece is not None
                and self.board[move_position].piece.player == self.player):
            return

        yield MoveOption(self.position, captures=[move_position])

        
class CoolerPiece(CoolPiece):
    """
    A piece that can move one square diagonally (down and right) and turn into a Queen when capturing another cool piece.
    """
    def __init__(self):
        super().__init__()
        # When listening to yourself, it's a good practice to use a high priority,
        # to emulate being the default behavior of the piece.
        self.subscribe(AfterMoveEvent, self._on_after_move, EventPriority.VERY_HIGH)

    @classmethod
    @property
    def name(cls):
        return "CoolerPiece"

    def _get_move_options(self) -> Iterable[MoveOption]:
        move_options = super()._get_move_options()
        for move_option in move_options:  
            if isinstance(self.board[move_option.position].piece, CoolPiece):
                move_option.extra = dict(turn_into_queen=True)
                yield move_option
            
    def _on_after_move(self, event: AfterMoveEvent):
        if event.move_option.extra.get("turn_into_queen"):
            # To make this extendable, it's a good practice to send Before and After events for this "promotion".
            self.board[event.move_option.position].piece = Queen(self.player)
```

## Rule

A rule is a class that can be used to add custom logic to the game.
It is also an abstract class, and must be extended to be used.

A rule should define startup logic in `on_join_board` - and only startup logic (e.g. subscribing to events).
The board passed shouldn't be kept in state - instead, callbacks should use the board from the event.
(This is again related to cloneables, and will be explained in the next section.)

An `as_rule` method is provided to turn a function into a rule, which is useful for stateless rules.

```python
def my_simple_rule(board: Board):
    
    def _on_before_move(event: BeforeMoveEvent):
        if isinstance(event.piece, Pawn):
            event.set_cancelled(True)
            
    board.subscribe(BeforeMoveEvent, _on_before_move)
    
MySimpleRule = as_rule(my_simple_rule)
    
class MyComplexRule(Rule):
    def __init__(self):
        self.moves = 0
        
    def _on_before_move(self, event: BeforeMoveEvent):
        self.moves += 1
        if self.moves < 3 and isinstance(event.piece, Pawn):
            event.set_cancelled(True)
            
    def on_join_board(self, board: Board):
        board.subscribe(BeforeMoveEvent, self._on_before_move)

board = Board(
    ...,
    rules = [MySimpleRule, MyComplexRule],
)
```

    
     