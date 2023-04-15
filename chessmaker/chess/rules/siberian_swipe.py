from itertools import chain

from chessmaker.chess.base.board import AfterNewPieceEvent, Board
from chessmaker.chess.base.move_option import MoveOption
from chessmaker.chess.base.piece import Piece, BeforeGetMoveOptionsEvent
from chessmaker.chess.base.rule import Rule
from chessmaker.chess.piece_utils import is_in_board
from chessmaker.chess.pieces.rook import Rook
from chessmaker.events import EventPriority


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
        rook: Rook = event.piece
        board = event.piece.board
        player = event.piece.player
        position = event.piece.position
        new_move_options = []

        if rook.moved:
            return

        for direction in [(0, 1), (0, -1)]:
            enemy_position = position.offset(*direction)

            while is_in_board(board, enemy_position):
                enemy_piece = board[enemy_position].piece

                if isinstance(enemy_piece, Rook) and enemy_piece.player != player:
                    move_option = MoveOption(enemy_position, captures={enemy_position}, extra=dict(siberian_swipe=True))
                    new_move_options.append(move_option)

                enemy_position = enemy_position.offset(*direction)

        event.set_move_options(chain(move_options, new_move_options))

    def clone(self):
        return SiberianSwipe()
