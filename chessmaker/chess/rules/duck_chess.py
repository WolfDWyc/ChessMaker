from itertools import chain

from chessmaker.chess.base import Board, as_rule, BeforeTurnChangeEvent
from chessmaker.chess.pieces.duck import Duck
from chessmaker.events import EventPriority


def on_before_turn_change(event: BeforeTurnChangeEvent):
    current_player = event.board.current_player
    if current_player != event.next_player:
        duck: Duck = [piece for piece in event.board.get_pieces() if isinstance(piece, Duck)][0]
        if duck.movable:
            duck.movable = False
            duck.player = event.next_player
        else:
            event.board.turn_iterator = chain([event.next_player], event.board.turn_iterator)
            event.set_next_player(current_player)
            duck.movable = True


def duck_chess(board: Board):
    board.subscribe(BeforeTurnChangeEvent, on_before_turn_change, EventPriority.HIGH)


DuckChess = as_rule(duck_chess)
