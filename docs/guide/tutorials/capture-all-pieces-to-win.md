# Capture All Pieces to Win

## Introduction

Out of all custom rules we'll cover, this is probably the simplest one.

We're going to create a new result function - `capture_all_pieces_to_win`,
it accepts a board and returns a descriptive string if the game is over -
otherwise it returns `None`.

## Creating the result function

```python title="capture_all_pieces_to_win.py"
from chessmaker.chess.base import Board


def capture_all_pieces_to_win(board: Board) -> str | None: 
    lost_players = []
    for player in board.players: 
        if len(list(board.get_player_pieces(player))) == 0: # (1)
            lost_players.append(player)

    if len(lost_players) == 0: # (2)
        return None

    if len(lost_players) == 1: # (3)
        return f"All pieces captured - {lost_players[0].name} loses"

    return "Multiple players have no pieces - Draw" # (4)
```

1. We check if the player has any pieces left.
2. If no players have lost, the game is not over - we return `None`.
3. If only one player has no pieces, we return a string saying that they have lost.
We specifically check for 1 player to support a custom rule that could allow a piece to destroy
itself - causing both players to have no pieces left.
4. If both players have no pieces, we return a string saying that the game is a draw.

Then, when we create a new game, we can pass this function to the `result_function` argument:

```python
game = Game(
    board=...,
    get_result=capture_all_pieces_to_win,
)
```

And that's it! We can now play a game where the only winning condition is to capture all pieces.

## Adding other result functions

Even though we don't want to be able to win by checkmate in this variant,
we might still want to have stalemate, repetition and other result functions.

To do this, we can change our result function to a class, and add in other results:

```python
from chessmaker.chess.results import stalemate, Repetition, NoCapturesOrPawnMoves

class CaptureAllPiecesToWin:
    def __init__(self):
        self.result_functions = [capture_all_pieces_to_win, stalemate, Repetition(), NoCapturesOrPawnMoves()]

    def __call__(self, board: Board):
        for result_function in self.result_functions:
            result = result_function(board)
            if result:
                return result
```

!!! note
    Results that hold state (like repitition or compuond results like ours) should always be classes
    (and not functions), so they can be copied.

## Removing checks

For a game mode like this, starting with a king is not required
(though it's still possible to do so).

However, if we would want to start with a king that can't be checked,
we would have to change some more things when initializing the board.

Thankfully, the default King implementation supports an `attackable` argument
(which defaults to False), so we can just set it to true:

```python
_king = lambda player: King(player, attackable=True)

game = Game(
    board=Board(
        squares=[
            [Square(_king(black)), ...],
            ...
        ],  
        ...
    )
    get_result=capture_all_pieces_to_win,
)
```

??? note "What if the king didn't have an `attackable` argument?"
    In this case, it was convenient that the King class had an `attackable` argument
    (for another purpose), but how would we implement this if it didn't? Because a custom
    king implementation is a lot of work, we could just inherit from the default King class.
    It would require looking a bit at the source code - but we would quickly see the
    startup logic for the King's check handling is done in `on_join_board`, so we would just override it:
    ```python
    def AttackableKing(King):
        def on_join_board(self, board: Board):
            pass
    ```


