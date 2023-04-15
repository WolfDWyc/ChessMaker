# Cloneables

## Introduction

While ChessMaker isn't dependent on any specific chess rule or piece,
there some concepts that are mainly used by one piece in the standard game.

One of these is that everything in the board (e.g. everything besides the Game object)
has a `clone` method, which returns a copy of the object.

In the standard game, this is only used for the King implementation (Though it could be useful for
other custom rules too) - so while most your rules and pieces won't have to use the clone method,
they all have to implement it.

??? info
    Because a game doesn't have to include a king, other pieces aren't aware of the concepts of
    check and checkmate. This means the king subscribes to `BeforeGetMoveOptionsEvent` events
    of all pieces, and checks if any of those moves would make it attacked by simulating
    the move in a cloned board. Simulation is necessary because of custom rules.
    For example - a custom piece could theoretically define that if the King
    moved near it - it would turn into a queen. This means just looking at the move options
    and not actually moving the piece would cause incorrect results.
    
## What is Cloneable?

- The board
- Squares
- Pieces
- Rules

The board and squares don't really interest us, since they aren't meant to be extended.
So let's focus on pieces and rules.

## Pieces

### Stateless pieces

Even stateless pieces have to implement the clone method - while this could be implemented
by the base piece class, making all pieces do it makes it harder to forget when 
implementing a stateful piece. The is how it would look:

```python
class CoolPiece(Piece):
    def clone(self):
        return CoolPiece(self.player)
```

### Stateful pieces

The simplest example for this is the Rook.
While the Rook is a fairly simple piece, it has to know if it has moved or not.
This is because it can only castle if it hasn't moved yet.

```python
class Rook(Piece):
    def __init__(self, player, moved=False):
        super().__init__(player)
        self._moved = moved

    # Some rook logic...
        
    def clone(self):
        return Rook(self.player, self._moved)
```

### Inheriting from other pieces

If you're inheriting from another piece, you should reimplement the clone method.
```python
class CoolerPiece(CoolPiece):
    def clone(self):
        return CoolerPiece(self.player)
```

## Rules

For rules, it's about the same - but a bit easier.

### Stateless rules

If your rule doesn't have any state, it should be a function that uses
the `as_rule` helper function anyway - so you don't have to implement the clone method.

```python
def my_simple_rule(board: Board):
    # Some rule logic...

MySimpleRule = as_rule(my_simple_rule)
```

### Stateful rules

If your rule has state, you should implement the clone method.

```python
class ExtraTurnOnFirstKingMove(Rule):

    def __init__(self, player_king_moved: dict[Player, bool] = None):
        if player_king_moved is None:
            player_king_moved = defaultdict(bool)
        self.player_king_moved: dict[Player, bool] = player_king_moved


    def _on_after_move(event: AfterMoveEvent):
        if not self.player_king_moved[event.piece.player] and isinstance(event.piece, King):
            event.board.turn_iterator = chain(
                [event.board.current_player],
                event.board.turn_iterator,
            )
            self.player_king_moved[event.piece.player] = True
    
            
    def on_join_board(self, board: Board):
        board.subscribe(AfterMoveEvent, self._on_after_move, EventPriority.HIGH)

        
    def clone(self):
        return ExtraTurnOnFirstKingMove(self.player_king_moved.copy())
```

## Why not just deepcopy?

If you're wondering why ChessMaker doesn't just use `copy.deepcopy` - it's because
deepcopy would copy all attributes, including event subscriptions - which is not
what we want.