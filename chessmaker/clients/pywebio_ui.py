from copy import deepcopy
from dataclasses import dataclass, field
from itertools import groupby
from typing import Callable, List, ParamSpec, TypeVar, Optional, Any
from uuid import uuid4

from pywebio import start_server, config
from pywebio.input import input_group, actions, checkbox, radio
from pywebio.io_ctrl import Output
from pywebio.output import put_text, put_table, put_markdown, put_button, use_scope, clear, put_scope, popup, \
    close_popup, toast, put_error
from pywebio.session import local as session_data, ThreadBasedSession, eval_js
from pywebio_battery import get_query

from chessmaker.chess.base.board import Board
from chessmaker.chess.base.game import Game, AfterTurnChangeEvent, AfterGameEndEvent
from chessmaker.chess.base.move_option import MoveOption
from chessmaker.chess.base.piece import Piece, AfterMoveEvent
from chessmaker.chess.base.player import Player
from chessmaker.chess.base.position import Position
from chessmaker.chess.base.square import Square
from chessmaker.chess.game_factory import create_game

CSS = """
.pywebio {padding-top: 0} .markdown-body table {display:table; width:250px; margin:10px auto;}
.markdown-body table th {padding:0;}
.markdown-body p {margin:0;}
.markdown-body table td {font-weight:bold; padding:0; line-height:80px; border: 0}
.markdown-body table tr {border: 0}
td>div {width:80px; height:80px}.btn-light {background-color:#d3d6da;}
@media (max-width: 435px) {.btn{padding:0.375rem 0.5rem;}}
@media (max-width: 355px) {.btn{padding:0.375rem 0.4rem;}}
div[id='pywebio-scope-board'] .btn {width: 80px; height: 80px;}
.pywebio {min-height:calc(100vh - 50px);}
div[id$="-move-option"] button {color: #bdc6c8; display: inline-flex; align-item: flex-start;
 vertical-align: top; padding: 0px; line-height: 0.75; font-style: italic; font-size: 11px;
 white-space: nowrap;}
"""


@dataclass
class MultiplayerGame:
    game: Game
    options: list[str]
    sessions: List[ThreadBasedSession] = field(default_factory=list)
    colors: dict[str, str] = field(default_factory=dict)


multiplayer_games: dict[str, MultiplayerGame] = {}

piece_types = {
    "Pawn": "p",
    "Rook": "r",
    "Knight": "n",
    "Bishop": "b",
    "Queen": "q",
    "King": "k"
}

PS = ParamSpec("PS")
RT = TypeVar("RT")

def for_all_game_sessions(func: Callable[PS, RT]) -> Callable[PS, RT]:
    game_id = session_data.game_id

    def wrapper(*args, **kwargs):
        game = multiplayer_games[game_id]
        for session in game.sessions:
            func_id = str(uuid4())

            def inner(_):
                func(*args, **kwargs)

            session.callbacks[func_id] = (inner, False)
            session.callback_mq.put({"task_id": func_id, "data": None})

    return wrapper


def clear_move_options():
    board: Board = session_data.game.board
    if session_data.shown_move_options is not None:
        for move_option in session_data.shown_move_options:
            position = move_option.position
            clear(str(position))
            with use_scope(str(position), clear=True):
                put_scope(str(uuid4()), square_content(board[position]))
        session_data.shown_move_options = None
        session_data.clicked_position = None


def get_piece_url(piece: Piece):
    piece_color = multiplayer_games[session_data.game_id].colors[piece.player.name]
    if piece.name == "Knook":
        if piece_color == "w":
            return "https://i.imgur.com/UiWcdEb.png"
        else:
            return "https://i.imgur.com/g7xTVts.png"

    piece_type = piece_types[piece.name]

    return f"https://www.chess.com/chess-themes/pieces/neo/150/{piece_color}{piece_type}.png"


def show_multiple_move_options(piece: Piece, move_options: List[MoveOption]):
    with popup("Choose an option"):
        for move_option in move_options:
            def on_click(_move_option=deepcopy(move_option)):
                piece.move(_move_option)
                close_popup()

            if move_option.extra:
                text = ", ".join([f"{key.title()}: {value}" for key, value in move_option.extra.items()])
            else:
                text = "Move"

            button = put_button(text, onclick=on_click)
            button.style("width: 100%")


@use_scope("board")
def show_move_options(position: Position):
    clear_move_options()
    board: Board = session_data.game.board
    piece = board[position].piece

    sorted_move_options = sorted(piece.get_move_options(), key=lambda move_option: move_option.position)
    grouped_move_options = groupby(sorted_move_options, key=lambda move_option: move_option.position)

    for move_option_position, position_move_options in grouped_move_options:
        position_move_options = list(position_move_options)

        with use_scope(str(move_option_position), clear=True):
            with use_scope(f"{move_option_position}-move-option"):

                text = ""
                if len(position_move_options) == 1:
                    move_option = position_move_options[0]
                    on_click = lambda _move_option=move_option: piece.move(_move_option)
                    if move_option.extra:
                        text = list(move_option.extra.keys())[0].capitalize().replace("_", " ")
                else:
                    on_click = lambda _move_options=position_move_options: show_multiple_move_options(piece,
                                                                                                      _move_options)
                    text = "Multiple options"

                content = put_button(text, color="transparent", onclick=on_click)


                move_option_position_piece = board[move_option_position].piece
                if move_option_position_piece is not None:
                    content.style(f"background-image: url({get_piece_url(move_option_position_piece)});")

                content.style("width:80px")
                content.style("height:80px")
                content.style("background-size: 100%;")
                content.style("background-color: #3c93f2") # #4bb543
                content.style("box-sizing: content-box")
                content.style("border: 0.5px solid #aaaaaa")

    session_data.shown_move_options = sorted_move_options
    session_data.clicked_position = position


def on_piece_click(position: Position):
    board: Board = session_data.game.board
    if session_data.clicked_position == position:
        clear_move_options()
        return

    current_player: Player = board.current_player
    if current_player != board[position].piece.player:
        return

    if session_data.player != "":
        if session_data.player != current_player:
            return
        if len(multiplayer_games[session_data.game_id].sessions) < 2:
            toast("Waiting for another player to join...", position="top", duration=3)
            return

    show_move_options(position)


@use_scope("board")
def square_content(square: Square):

    content = put_text(" ")
    content.style("white-space: nowrap;")
    if square is None:
        content = content.style("background-color: #ffffff")
        content = content.style("width:80px")
        content = content.style("height:80px")
    else:
        piece = square.piece
        if piece is not None:
            content = put_button("", color="transparent", onclick=lambda: on_piece_click(piece.position))
            content.style("white-space: nowrap;")
            content.style(f"background-image: url({get_piece_url(piece)});")
            content.style("background-size: 100%;")

    return content

def get_board_strings(board: Board) -> dict[Position, Optional[str]]:
    board_strings = {}
    for y in range(board.size[1]):
        for x in range(board.size[0]):
            square = board[Position(x, y)]
            if square is None:
                board_strings[Position(x, y)] = None
            else:
                board_strings[Position(x, y)] = str(id(square.piece))
    return board_strings


def on_after_move(event: AfterMoveEvent):
    clear_move_options()
    board: Board = session_data.game.board
    last_board_pieces = session_data.last_board_pieces
    board_pieces = get_board_strings(board)

    for position, piece in board_pieces.items():
        last_piece = last_board_pieces.get(position)
        if piece != last_piece:
            clear(str(position))
            with use_scope(str(position), clear=True):
                put_scope(str(uuid4()), square_content(board[position]))

    session_data.last_board_pieces = board_pieces
    toast(f"{event.piece.player.name.capitalize()} moved", position="top", duration=3)


def on_after_turn_change(event: AfterTurnChangeEvent):
    # TODO: What if the second turn is the same player?
    if session_data.player is None and not session_data.own_game:
        session_data.player = event.player


def on_game_end(event: AfterGameEndEvent):
    popup("Game Over", event.result)


def initialize_board():
    board: Board = session_data.game.board
    options = multiplayer_games[session_data.game_id].options
    if options:
        put_text(f"Options: {', '.join(options)}")

    with use_scope("board"):
        grid: list[list[Output | None]] = [[None for _ in range(board.size[0])] for _ in range(board.size[1])]

        for y in range(board.size[1]):
            for x in range(board.size[0]):
                position = Position(x, y)
                square = board[position]

                scope = put_scope(str(position), content=square_content(square))

                if square is not None:
                    if (position[0] + position[1]) % 2 == 0:
                        scope.style("background-color: #f0d9b5")
                    else:
                        scope.style("background-color: #b58863")

                if session_data.own_game:
                    grid[y][x] = scope
                else:
                    grid[board.size[1] - y - 1][x] = scope

        for index in range(board.size[1]):
            number = board.size[1] - index if session_data.own_game else index + 1
            grid[index].insert(0, put_text(str(number)))
        grid.insert(0, [put_text()] + [put_text(chr(index + 65)) for index in range(board.size[0])])

        put_table(grid).style("text-align: center")

    session_data.last_board_pieces = get_board_strings(board)

def join_game(game_id: str):
    multiplayer_games[game_id].sessions.append(ThreadBasedSession.get_current_session())
    game = multiplayer_games[game_id].game

    session_data.game = game
    session_data.game_id = game_id
    session_data.own_game = False

    initialize_board()

def new_game(game_factory: Callable[..., Game], options: list[str], mode: str):
    game: Game = game_factory(**{option: True for option in options})
    game_id = str(uuid4())

    session_data.game = game
    session_data.game_id = game_id

    multiplayer_game = MultiplayerGame(game, options, [ThreadBasedSession.get_current_session()])
    colors = ['w', 'b']
    for player in game.board.players:
        multiplayer_game.colors[player.name] = colors.pop(0)

    multiplayer_games[game_id] = multiplayer_game

    session_data.own_game = True
    if mode == 'Multiplayer':
        session_data.player = game.board.current_player
    else:
        session_data.player = ""

    # game.board.subscribe(AfterAddPieceEvent, for_all_game_sessions(on_after_change_piece))
    # game.board.subscribe(AfterRemovePieceEvent, for_all_game_sessions(on_after_change_piece))
    game.board.subscribe(AfterMoveEvent, for_all_game_sessions(on_after_move))
    game.board.subscribe(AfterTurnChangeEvent, for_all_game_sessions(on_after_turn_change))
    game.subscribe(AfterGameEndEvent, for_all_game_sessions(on_game_end))

    put_markdown("# Chess \n").style("text-align:center")
    if mode == 'Multiplayer':
        put_text("Invite URL: " + eval_js("window.location.href.split('?')[0]") + "?game_id=" + session_data.game_id)
    initialize_board()


def start_pywebio_chess_server(
        game_factory: Callable[..., Game],
        supported_options: List[str] = None,
        remote_access: bool = False,
        port: int = 8080,
        debug: bool = False,
):
    if supported_options is None:
        supported_options = []

    @config(title="Chess", css_style=CSS)
    def main():
        if get_query("game_id"):
            if get_query("game_id") not in multiplayer_games:
                popup("Error", put_error("Game not found"))
            else:
                join_game(get_query("game_id"))
            return
        form_result = input_group('New Game', [
            radio('Mode', ['Singleplayer', 'Multiplayer'], name='mode', value='Multiplayer'),
            checkbox('Options',
                     options=supported_options,
                     name='options'),
            actions('-', [
                {'label': 'Create ', 'value': 'create'},
            ], name='action'),
        ])

        new_game(game_factory, form_result['options'], form_result['mode'])

    start_server(main, port=port, remote_access=remote_access, debug=debug)


if __name__ == "__main__":
    start_pywebio_chess_server(create_game, ["chess960", "knooks", "force_en_passant", "knight_boosting", "omnipotent_f6_pawn",
                              "siberian_swipe", "il_vaticano", "beta_decay"], debug=True)
