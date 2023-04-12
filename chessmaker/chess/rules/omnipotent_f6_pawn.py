from typing import Callable

from chessmaker.chess.base.board import Board
from chessmaker.chess.base.move_option import MoveOption
from chessmaker.chess.base.piece import Piece, BeforeGetMoveOptionsEvent, BeforeMoveEvent
from chessmaker.chess.base.player import Player
from chessmaker.chess.base.position import Position
from chessmaker.chess.base.rule import Rule
from chessmaker.events import EventPriority

F6 = Position(5, 2)

class OmnipotentF6Pawn(Rule):
    def __init__(self, player_to_pawn: dict[Player, Callable[[], Piece]]):
        self.player_to_pawn = player_to_pawn

    def on_join_board(self, board: Board):
        board.subscribe(BeforeGetMoveOptionsEvent, self.on_before_get_move_options, EventPriority.HIGH)
        board.subscribe(BeforeMoveEvent, self.on_before_move)

    def on_before_get_move_options(self, event: BeforeGetMoveOptionsEvent):
        f6_piece = event.piece.board[F6].piece

        if f6_piece is not None and f6_piece.player != event.piece.player:
            move_options = list(event.move_options)
            move_options.append(MoveOption(F6, extra=dict(summon_pawn=True), captures={F6}))
            event.set_move_options(move_options)

    def on_before_move(self, event: BeforeMoveEvent):
        if event.move_option.extra.get("summon_pawn"):
            piece = self.player_to_pawn[event.piece.player]()
            event.piece.board[F6].piece = piece
            piece.move(MoveOption(F6))
            event.set_move_option(MoveOption(event.piece.position))
            event.set_cancelled(True)

    def clone(self):
        return OmnipotentF6Pawn(player_to_pawn=self.player_to_pawn)



