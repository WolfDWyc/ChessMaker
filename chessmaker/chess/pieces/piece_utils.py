from typing import Iterable

from chessmaker.chess.base.board import Board
from chessmaker.chess.base.move_option import MoveOption
from chessmaker.chess.base.piece import Piece
from chessmaker.chess.base.position import Position


def is_in_board(board: Board, position: Position) -> bool:
    if position.x < 0 or position.x >= board.size[0] or position.y < 0 or position.y >= board.size[1]:
        return False

    new_square = board[position]
    if new_square is None:
        return False

    return True


def iterate_until_blocked(piece: Piece, direction: tuple[int, int]) -> Iterable[Position]:
    board = piece.board
    position = piece.position

    i = 1
    while True:
        new_position = position.offset(direction[0] * i, direction[1] * i)
        if not is_in_board(board, new_position):
            break

        new_square = board[new_position]
        if new_square.piece is not None:
            yield new_position
            break

        yield new_position
        i += 1


def get_diagonals_until_blocked(piece: Piece) -> Iterable[Position]:
    for direction in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
        yield from iterate_until_blocked(piece, direction)


def get_horizontal_until_blocked(piece: Piece) -> Iterable[Position]:
    for direction in [(1, 0), (-1, 0)]:
        yield from iterate_until_blocked(piece, direction)


def get_vertical_until_blocked(piece: Piece) -> Iterable[Position]:
    for direction in [(0, 1), (0, -1)]:
        yield from iterate_until_blocked(piece, direction)


def get_straight_until_blocked(piece: Piece) -> Iterable[Position]:
    yield from get_horizontal_until_blocked(piece)
    yield from get_vertical_until_blocked(piece)


def filter_uncapturable_positions(piece: Piece, positions: Iterable[Position]) -> Iterable[Position]:
    filtered_positions = []
    for position in positions:
        position_piece = piece.board[position].piece
        if position_piece is not None and position_piece.player == piece.player:
            continue
        filtered_positions.append(position)

    return filtered_positions

def positions_to_move_options(board: Board, positions: Iterable[Position]) -> Iterable[MoveOption]:
    for position in positions:
        if board[position].piece is None:
            yield MoveOption(position)
        else:
            yield MoveOption(position, captures={position})
