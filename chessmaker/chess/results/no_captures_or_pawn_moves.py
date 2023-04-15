from chessmaker.chess.base import Board
from chessmaker.chess.pieces import Pawn


class NoCapturesOrPawnMoves:
    def __init__(self, needed_moves: int = 50):
        self.needed_moves = needed_moves
        self.last_pawn_positions = None
        self.last_piece_ids = -1
        self.last_change = 0

    def __call__(self, board: Board) -> str | None:
        current_player = board.current_player
        player_pieces = list(board.get_player_pieces(current_player))

        pawn_positions = [piece.position for piece in player_pieces if isinstance(piece, Pawn)]
        piece_ids = set(map(id, player_pieces))
        if self.last_pawn_positions is not None and self.last_pawn_positions != pawn_positions:
            self.last_change = 0
        elif self.last_piece_ids != -1 and self.last_piece_ids != piece_ids:
            self.last_change = 0
        else:
            self.last_change += 1

        if self.last_change >= self.needed_moves:
            return f"{self.needed_moves} move rule - Draw"

        self.last_pawn_positions = pawn_positions
        self.last_piece_ids = piece_ids
