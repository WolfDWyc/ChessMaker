from collections import defaultdict

from chessmaker.chess.base.board import Board
from chessmaker.chess.base.game import AfterTurnChangeEvent
from chessmaker.chess.base.piece import BeforeGetMoveOptionsEvent
from chessmaker.chess.base.player import Player
from chessmaker.chess.base.rule import Rule
from chessmaker.chess.pieces.pawn import Pawn
from chessmaker.events import EventPriority


class ForcedEnPassant(Rule):
    def __init__(self, can_en_passant: dict[Player, bool] = None):
        if can_en_passant is None:
            can_en_passant = defaultdict(lambda: False)
        self.can_en_passant: dict[Player, bool] = can_en_passant

    def on_join_board(self, board: Board):
        board.subscribe(BeforeGetMoveOptionsEvent, self.on_before_get_move_options, EventPriority.LOW)
        board.subscribe(AfterTurnChangeEvent, self.on_turn_change)

    def on_turn_change(self, event: AfterTurnChangeEvent):
        for player in event.board.players:
            self.can_en_passant[player] = False
            for piece in event.board.get_player_pieces(player):
                if isinstance(piece, Pawn):
                    move_options = piece._get_move_options()
                    if any(move_option.extra.get("en_passant") for move_option in move_options):
                        self.can_en_passant[player] = True
                        break

    def on_before_get_move_options(self, event: BeforeGetMoveOptionsEvent):
        event_move_options = event.move_options
        if not self.can_en_passant[event.piece.player]:
            return
        move_options = []
        for move_option in event_move_options:
            if move_option.extra.get("en_passant"):
                move_options.append(move_option)
        event.set_move_options(move_options)

    def clone(self):
        return ForcedEnPassant(can_en_passant=self.can_en_passant.copy())



