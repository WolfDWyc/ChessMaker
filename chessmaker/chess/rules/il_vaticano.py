from itertools import chain

from chessmaker.chess.base.board import Board, AfterNewPieceEvent
from chessmaker.chess.base.move_option import MoveOption
from chessmaker.chess.base.piece import Piece, BeforeGetMoveOptionsEvent, BeforeMoveEvent
from chessmaker.chess.base.rule import Rule
from chessmaker.chess.pieces.bishop import Bishop
from chessmaker.chess.pieces.piece_utils import is_in_board
from chessmaker.events import EventPriority

SIZE = 3
sign = lambda x: x and (1, -1)[x < 0]

class IlVaticano(Rule):
    def on_join_board(self, board: Board):
        for piece in board.get_pieces():
            self.subscribe_to_piece(piece)

        board.subscribe(AfterNewPieceEvent, self.on_new_piece)

    def subscribe_to_piece(self, piece: Piece):
        if isinstance(piece, Bishop):
            piece.subscribe(BeforeGetMoveOptionsEvent, self.on_before_get_move_options, EventPriority.HIGH)
            piece.subscribe(BeforeMoveEvent, self.on_before_move)

    def on_new_piece(self, event: AfterNewPieceEvent):
        self.subscribe_to_piece(event.piece)

    def on_before_get_move_options(self, event: BeforeGetMoveOptionsEvent):
        move_options = event.move_options

        piece = event.piece
        player = piece.player
        board = piece.board
        position = piece.position
        for offset in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            other_position = position.offset(offset[0] * SIZE, offset[1] * SIZE)
            if not is_in_board(board, other_position):
                continue

            other_piece = board[other_position].piece
            if not isinstance(other_piece, Bishop) or other_piece.player != player:
                continue

            enemy_positions = []
            for i in range(1, SIZE):
                enemy_position = position.offset(offset[0] * i, offset[1] * i)
                if not is_in_board(board, enemy_position):
                    continue

                enemy = board[enemy_position].piece
                if enemy is None or enemy.player == player:
                    continue

                enemy_positions.append(enemy_position)

            if len(enemy_positions) == SIZE - 1:
                move_option = MoveOption(other_position, extra=dict(il_vaticano=True), captures=set(enemy_positions))
                move_options = chain(move_options, [move_option])

        event.set_move_options(move_options)

    def on_before_move(self, event: BeforeMoveEvent):
        piece = event.piece
        board = piece.board
        position = piece.position
        if "il_vaticano" in event.move_option.extra:
            other_position = event.move_option.position

            # Iterate all positions between the two positions
            direction = (sign(other_position.x - position.x), sign(other_position.y - position.y))
            enemy_position = position.offset(*direction)
            while enemy_position != other_position:
                board[enemy_position].piece = None
                enemy_position = enemy_position.offset(*direction)

            board[position].piece = board[other_position].piece
            board[other_position].piece = piece
            piece.move(MoveOption(other_position))
            event.set_cancelled(True)
    def clone(self):
        return IlVaticano()



