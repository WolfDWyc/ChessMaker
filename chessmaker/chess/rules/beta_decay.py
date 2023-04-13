from itertools import chain
from typing import Callable

from chessmaker.chess.base.board import AfterNewPieceEvent, Board
from chessmaker.chess.base.move_option import MoveOption
from chessmaker.chess.base.piece import Piece, BeforeGetMoveOptionsEvent, BeforeMoveEvent, AfterMoveEvent
from chessmaker.chess.base.player import Player
from chessmaker.chess.base.rule import Rule
from chessmaker.chess.pieces.piece_utils import iterate_until_blocked
from chessmaker.chess.pieces.queen import Queen
from chessmaker.events import EventPriority

sign = lambda x: x and (1, -1)[x < 0]

class BetaDecay(Rule):
    def __init__(self, decay_to_pieces: list[Callable[[Player], Piece]]):
        self.decay_to_pieces: list[Callable[[Player], Piece]] = decay_to_pieces

    def on_join_board(self, board: Board):
        for piece in board.get_pieces():
            self.subscribe_to_piece(piece)

        board.subscribe(AfterNewPieceEvent, self.on_new_piece)

    def subscribe_to_piece(self, piece: Piece):
        if isinstance(piece, Queen):
            piece.subscribe(BeforeGetMoveOptionsEvent, self.on_before_get_move_options, EventPriority.HIGH)
            piece.subscribe(BeforeMoveEvent, self.on_before_move)

    def on_new_piece(self, event: AfterNewPieceEvent):
        self.subscribe_to_piece(event.piece)

    def on_before_get_move_options(self, event: BeforeGetMoveOptionsEvent):
        move_options = event.move_options
        piece = event.piece
        board = piece.board
        for direction in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            positions = list(iterate_until_blocked(piece, direction))
            if len(positions) == 0:
                continue

            last_position = positions[-1]
            if board[last_position].piece is not None:
                if board[last_position].piece.player != piece.player:
                    continue
                last_position = last_position.offset(direction[0] * -1, direction[1] * -1)

            if (abs(last_position.x - piece.position.x) < len(self.decay_to_pieces) and
                    abs(last_position.y - piece.position.y) < len(self.decay_to_pieces)):
                continue

            move_option = MoveOption(last_position, extra=dict(beta_decay=True))
            move_options = chain(move_options, [move_option])

        event.set_move_options(move_options)

    def on_before_move(self, event: BeforeMoveEvent):
        if "beta_decay" in event.move_option.extra:
            piece = event.piece
            board = piece.board
            position = event.piece.position
            other_position = event.move_option.position

            direction = (sign(other_position.x - position.x), sign(other_position.y - position.y))
            distance = max(abs(other_position.x - position.x), abs(other_position.y - position.y))
            start_distance = distance - len(self.decay_to_pieces) + 1
            start_position = position.offset(direction[0] * start_distance, direction[1] * start_distance)
            for i, create_piece in enumerate(self.decay_to_pieces):
                new_piece_position = start_position.offset(direction[0] * i, direction[1] * i)
                board[new_piece_position].piece = create_piece(piece.player)

            board[position].piece = None
            piece.publish(AfterMoveEvent(piece, event.move_option))
            event.set_cancelled(True)

    def clone(self):
        return BetaDecay(self.decay_to_pieces)
