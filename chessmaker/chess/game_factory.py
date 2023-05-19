import random
from itertools import cycle
from typing import Callable

from chessmaker.chess import results
from chessmaker.chess.base.board import Board
from chessmaker.chess.base.game import Game
from chessmaker.chess.base.piece import Piece
from chessmaker.chess.base.player import Player
from chessmaker.chess.base.square import Square
from chessmaker.chess.pieces.bishop import Bishop
from chessmaker.chess.pieces.duck import Duck
from chessmaker.chess.pieces.king import King
from chessmaker.chess.pieces.knight import Knight
from chessmaker.chess.pieces.knook.knookable_knight import KnookableKnight
from chessmaker.chess.pieces.knook.knookable_rook import KnookableRook
from chessmaker.chess.pieces.pawn import Pawn
from chessmaker.chess.pieces.queen import Queen
from chessmaker.chess.pieces.rook import Rook
from chessmaker.chess.results import stalemate, Repetition, NoCapturesOrPawnMoves, checkmate, no_kings
from chessmaker.chess.rules import ForcedEnPassant, KnightBoosting, OmnipotentF6Pawn, SiberianSwipe, IlVaticano, \
    BetaDecay, KingCantMoveToC2, LaBastarda, DuckChess


class A:
    pass


def create_game(
        chess960: bool = False,
        knooks: bool = False,
        forced_en_passant: bool = False,
        knight_boosting: bool = False,
        omnipotent_f6_pawn: bool = False,
        siberian_swipe: bool = False,
        il_vaticano: bool = False,
        beta_decay: bool = False,
        la_bastarda: bool = False,
        king_cant_move_to_c2: bool = False,
        vertical_castling: bool = False,
        double_check_to_win: bool = False,
        capture_all_pieces_to_win: bool = False,
        duck_chess: bool = False,
):
    _knight = Knight
    _rook = Rook
    castling_directions = ((1, 0), (-1, 0))
    if vertical_castling:
        castling_directions = tuple(list(castling_directions) + [(0, 1), (0, -1)])
    attackable = capture_all_pieces_to_win or duck_chess
    _king = lambda player: King(player, attackable=attackable, castling_directions=castling_directions)
    if knooks:
        _knight = KnookableKnight
        _rook = KnookableRook

    white = Player("white")
    black = Player("black")
    turn_iterator = cycle([white, black])

    def _empty_line(length: int) -> list[Square]:
        return [Square() for _ in range(length)]

    def _pawn(player: Player):
        if player == white:
            return Pawn(white, Pawn.Direction.UP, promotions=[Bishop, _rook, Queen, _knight])
        elif player == black:
            return Pawn(black, Pawn.Direction.DOWN, promotions=[Bishop, _rook, Queen, _knight])

    def _piece_row() -> list[Callable[[Player], Piece]]:
        pieces = [_rook, _knight, Bishop, Queen, _king, Bishop, _knight, _rook]

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

                king = row.index(_king)
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
        (forced_en_passant, ForcedEnPassant()),
        (knight_boosting, KnightBoosting()),
        (siberian_swipe, SiberianSwipe()),
        (il_vaticano, IlVaticano()),
        (king_cant_move_to_c2, KingCantMoveToC2()),
        (omnipotent_f6_pawn, OmnipotentF6Pawn(pawn=_pawn)),
        (la_bastarda, LaBastarda(pawn=_pawn)),
        (beta_decay, BetaDecay([_rook, Bishop, _pawn])),
        (duck_chess, DuckChess()),
    ]:
        if enabled:
            rules.append(rule)

    result_functions = [stalemate, Repetition(3), NoCapturesOrPawnMoves(50)]
    if capture_all_pieces_to_win:
        result_functions.insert(0, results.capture_all_pieces_to_win)
    else:
        if not duck_chess:
            result_functions.insert(0, checkmate)
        result_functions.insert(0, no_kings)

    if double_check_to_win:
        result_functions.insert(0, results.double_check_to_win)

    class GetResult:
        def __init__(self):
            self.result_functions = result_functions

        def __call__(self, board: Board):
            for result_function in self.result_functions:
                result = result_function(board)
                if result:
                    return result

    game = Game(
        board=Board(
            squares=[
                [Square(piece_row[i](black)) for i in range(8)],
                [Square(_pawn(black)) for _ in range(8)],
                _empty_line(8),
                _empty_line(7) + [Square(Duck(white) if duck_chess else None)],
                _empty_line(8),
                _empty_line(8),
                [Square(_pawn(white)) for _ in range(8)],
                [Square(piece_row[i](white)) for i in range(8)],
            ],
            players=[white, black],
            turn_iterator=turn_iterator,
            rules=rules,
        ),
        get_result=GetResult(),
    )

    return game
