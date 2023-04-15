from chessmaker.chess.base import Board, as_rule, Position, BeforeGetMoveOptionsEvent, AfterNewPieceEvent, Piece
from chessmaker.chess.pieces import King
from chessmaker.events import EventPriority

C2 = Position(2, 6)


def on_before_get_move_options(event: BeforeGetMoveOptionsEvent):
    move_options = list(event.move_options)
    move_options = [move_option for move_option in move_options if move_option.position != C2]
    event.set_move_options(move_options)


def subscribe_to_piece(piece: Piece):
    if isinstance(piece, King):
        piece.subscribe(BeforeGetMoveOptionsEvent, on_before_get_move_options)


def on_after_new_piece(event: AfterNewPieceEvent):
    subscribe_to_piece(event.piece)


def king_cant_move_to_c2(board: Board):
    for piece in board.get_pieces():
        subscribe_to_piece(piece)
    board.subscribe(AfterNewPieceEvent, on_after_new_piece, EventPriority.LOW)


KingCantMoveToC2 = as_rule(king_cant_move_to_c2)
