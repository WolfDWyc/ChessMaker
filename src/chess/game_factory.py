import random
from itertools import cycle
from typing import Callable

from src.chess.base.board import Board
from src.chess.base.game import Game
from src.chess.base.piece import Piece
from src.chess.base.player import Player
from src.chess.base.square import Square
from src.chess.pieces.bishop import Bishop
from src.chess.pieces.king import King
from src.chess.pieces.knight import Knight
from src.chess.pieces.knook.knookable_knight import KnookableKnight
from src.chess.pieces.knook.knookable_rook import KnookableRook
from src.chess.pieces.pawn import Pawn
from src.chess.pieces.queen import Queen
from src.chess.pieces.rook import Rook
from src.chess.results.simple_result import GetSimpleResult
from src.chess.rules import ForceEnPassant, KnightBoosting, OmnipotentF6Pawn, SiberianSwipe, IlVaticano, BetaDecay

class A:
    pass

def create_game(
        chess960: bool = False,
        knooks: bool = False,
        force_en_passant: bool = False,
        knight_boosting: bool = False,
        omnipotent_f6_pawn: bool = False,
        siberian_swipe: bool = False,
        il_vaticano: bool = False,
        beta_decay: bool = False,
):
    _knight = Knight
    _rook = Rook
    if knooks:
        _knight = KnookableKnight
        _rook = KnookableRook

    def _empty_line(length: int) -> list[Square]:
        return [Square() for _ in range(length)]

    def _up_pawn(player: Player):
        return Square(Pawn(player, Pawn.Direction.UP, promotions=[Bishop, _rook, Queen, _knight]))

    def _down_pawn(player: Player):
        return Square(Pawn(player, Pawn.Direction.DOWN, promotions=[Bishop, _rook, Queen, _knight]))

    white = Player("white")
    black = Player("black")
    turn_iterator = cycle([white, black])

    def _piece_row() -> list[Callable[[Player], Piece]]:

        pieces = [_rook, _knight, Bishop, Queen, King, Bishop, _knight, _rook]

        if chess960:
            row = [None] * len(pieces)
            matched = False
            while not matched:
                matched = True
                row = random.sample(pieces, len(pieces))
                first_bishop, second_bishop = [i for i, piece in enumerate(row) if piece == Bishop]
                if first_bishop % 2 == second_bishop % 2:
                    matched = False
                    continue

                king = row.index(King)
                first_rook, second_rook = [i for i, piece in enumerate(row) if piece == _rook]

                if king < first_rook < second_rook or king > first_rook > second_rook:
                    matched = False
                    continue
        else:
            row = pieces

        return row

    piece_row = _piece_row()

    rules = []
    for enabled, rule in [
        (force_en_passant, ForceEnPassant()),
        (knight_boosting, KnightBoosting()),
        (siberian_swipe, SiberianSwipe()),
        (il_vaticano, IlVaticano()),
        (omnipotent_f6_pawn, OmnipotentF6Pawn({white: lambda: _up_pawn(white).piece, black: lambda: _down_pawn(black).piece})),
        (beta_decay, BetaDecay([_rook, Bishop,
            lambda player: _up_pawn(player).piece if player == white else _down_pawn(player).piece,
        ])),
    ]:
        if enabled:
            rules.append(rule)

    board = Board(
        squares=[
            [Square(piece_row[i](black)) for i in range(8)],
            [_down_pawn(black) for _ in range(8)],
            _empty_line(8),
            _empty_line(8),
            _empty_line(8),
            _empty_line(8),
            [_up_pawn(white) for _ in range(8)],
            [Square(piece_row[i](white)) for i in range(8)],
        ],
        players=[white, black],
        turn_iterator=turn_iterator,
        rules=rules,
    )

    game = Game(
        board=board,
        get_result=GetSimpleResult(),
    )

    return game

