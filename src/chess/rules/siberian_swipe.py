from itertools import chain

from src.chess.base.board import AfterNewPieceEvent, Board
from src.chess.base.move_option import MoveOption
from src.chess.base.piece import Piece, BeforeGetMoveOptionsEvent
from src.chess.base.rule import Rule
from src.chess.pieces.piece_utils import is_in_board
from src.chess.pieces.rook import Rook
from src.events import EventPriority


class SiberianSwipe(Rule):
    def on_join_board(self, board: Board):
        for piece in board.get_pieces():
            self.subscribe_to_piece(piece)

        board.subscribe(AfterNewPieceEvent, self.on_new_piece)

    def subscribe_to_piece(self, piece: Piece):
        if isinstance(piece, Rook):
            piece.subscribe(BeforeGetMoveOptionsEvent, self.on_before_get_move_options, EventPriority.HIGH)

    def on_new_piece(self, event: AfterNewPieceEvent):
        self.subscribe_to_piece(event.piece)

    def on_before_get_move_options(self, event: BeforeGetMoveOptionsEvent):
        move_options = event.move_options
        board = event.piece.board
        player = event.piece.player
        position = event.piece.position
        for direction in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            opposite_direction = (-direction[0], -direction[1])
            if is_in_board(board, position.offset(*opposite_direction)):
                continue

            enemy_position = position
            enemy = None
            while True:
                enemy_position = enemy_position.offset(*direction)
                if not is_in_board(board, enemy_position):
                    break
                if isinstance(board[enemy_position].piece, Rook) and board[enemy_position].piece.player != player:
                    enemy = board[enemy_position].piece
                    break

            if enemy is not None and not is_in_board(board, enemy_position.offset(*direction)):
                move_option = MoveOption(enemy_position, extra=dict(siberian_swipe=True), captures={enemy_position})
                move_options = chain(move_options, [move_option])

        event.set_move_options(move_options)

    def clone(self):
        return SiberianSwipe()
