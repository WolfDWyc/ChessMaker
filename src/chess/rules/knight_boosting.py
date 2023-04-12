from collections import defaultdict
from itertools import chain

from src.chess.base.board import AfterNewPieceEvent, Board
from src.chess.base.piece import Piece, BeforeGetMoveOptionsEvent, AfterMoveEvent
from src.chess.base.player import Player
from src.chess.base.position import Position
from src.chess.base.rule import Rule
from src.chess.pieces.knight import Knight
from src.chess.pieces.pawn import Pawn, AfterPromotionEvent
from src.events import EventPriority


class KnightBoosting(Rule):
    def __init__(self, boostable_knights: dict[Player, Position] = None):
        if boostable_knights is None:
            boostable_knights = defaultdict(lambda: None)
        self.boostable_knights: dict[Player, Position] = boostable_knights
    def on_join_board(self, board: Board):
        for piece in board.get_pieces():
            self.subscribe_to_piece(piece)

        board.subscribe(AfterNewPieceEvent, self.on_new_piece)
        board.subscribe(BeforeGetMoveOptionsEvent, self.on_before_get_move_options, EventPriority.LOW)
        board.subscribe(AfterMoveEvent, self.reset_knights_after_move, EventPriority.HIGH)

    def subscribe_to_piece(self, piece: Piece):
        if isinstance(piece, Pawn):
            piece.subscribe(AfterPromotionEvent, self.on_after_promotion)

    def on_new_piece(self, event: AfterNewPieceEvent):
        self.subscribe_to_piece(event.piece)

    def on_after_promotion(self, event: AfterPromotionEvent):
        promotion = event.promotion
        if isinstance(promotion, Knight):
            board = event.pawn.board
            current_player = board.current_player
            board.turn_iterator = chain(
                [current_player],
                board.turn_iterator,
            )
            event.pawn.subscribe(AfterMoveEvent, self.add_knight_after_move)

    def add_knight_after_move(self, event: AfterMoveEvent):
        self.boostable_knights[event.piece.player] = event.move_option.position
        event.piece.unsubscribe(AfterMoveEvent, self.add_knight_after_move)

    def reset_knights_after_move(self, _: AfterMoveEvent):
        self.boostable_knights = defaultdict(lambda: None)

    def on_before_get_move_options(self, event: BeforeGetMoveOptionsEvent):
        player = event.piece.player
        boostable_knight = self.boostable_knights[player]
        if boostable_knight is None:
            return

        if event.piece.position == boostable_knight:
            return

        event.set_move_options([])

    def clone(self):
        return KnightBoosting(self.boostable_knights.copy())
