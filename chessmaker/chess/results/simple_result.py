from collections import defaultdict
from typing import TYPE_CHECKING

from chessmaker.chess.base.board import Board
from chessmaker.chess.base.position import Position
from chessmaker.chess.pieces.king import King
from chessmaker.chess.pieces.pawn import Pawn

if TYPE_CHECKING:
    from chessmaker.chess.base.game import Game


class GetSimpleResult:
    def __init__(self):
        self.positions = defaultdict(int)
        self.last_pawn_positions = None
        self.last_piece_count = -1
        self.last_change = 0

    def __call__(self, board: Board) -> str | None:
        current_player = board.current_player
        player_pieces = list(board.get_player_pieces(current_player))
        can_move = False
        for piece in player_pieces:
            if piece.get_move_options():
                can_move = True
                break

        if not can_move:
            kings = [piece for piece in player_pieces if isinstance(piece, King)]
            if not kings or all(king.is_attacked() for king in kings):
                return f"Checkmate - {current_player.name} loses"
            else:
                return "Stalemate - Draw"

        position_hash = ""
        for y in range(board.size[1]):
            for x in range(board.size[0]):
                square = board[Position(x, y)]
                if square is None:
                    position_hash += "None"
                elif square.piece is None:
                    position_hash += "Empty"
                else:
                    position_hash += square.piece.__class__.__name__ + square.piece.player._id

        self.positions[position_hash] += 1
        if self.positions[position_hash] >= 3:
            return "Repetition - Draw"

        pawn_positions = [piece.position for piece in player_pieces if isinstance(piece, Pawn)]
        piece_count = len(list(board.get_pieces()))
        if self.last_pawn_positions is not None and self.last_pawn_positions != pawn_positions:
            self.last_change = 0
        elif self.last_piece_count != -1 and self.last_piece_count != piece_count:
            self.last_change = 0
        else:
            self.last_change += 1

        if self.last_change >= 50:
            return "50 move rule - Draw"

        self.last_pawn_positions = pawn_positions
        self.last_piece_count = piece_count

        return None


