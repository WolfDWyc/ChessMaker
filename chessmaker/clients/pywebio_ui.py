import time
from copy import deepcopy
from dataclasses import dataclass, field
from itertools import groupby
from typing import Callable, List, ParamSpec, TypeVar, Optional
from uuid import uuid4

from pywebio import start_server, config
from pywebio.input import input_group, actions, checkbox, radio
from pywebio.io_ctrl import Output
from pywebio.output import put_text, put_table, put_markdown, put_button, use_scope, clear, put_scope, popup, \
    close_popup, toast, put_error
from pywebio.session import local as session_data, ThreadBasedSession, run_js
from pywebio_battery import get_query

from chessmaker.chess.base.board import Board
from chessmaker.chess.base.game import Game, AfterTurnChangeEvent, AfterGameEndEvent
from chessmaker.chess.base.move_option import MoveOption
from chessmaker.chess.base.piece import Piece, AfterMoveEvent
from chessmaker.chess.base.player import Player
from chessmaker.chess.base.position import Position
from chessmaker.chess.base.square import Square
from chessmaker.chess.game_factory import create_game
from chessmaker.events import EventPriority

CSS = """
.pywebio {padding-top: 0} .markdown-body table {display:table; width:250px; margin:10px auto;}
.markdown-body table th {padding:0;}
.markdown-body p {margin:0;}
.markdown-body table td {font-weight:bold; padding:0; line-height:80px; border: 0}
.markdown-body table tr {border: 0}
td>div {width:80px; height:80px}.btn-light {background-color:#d3d6da;}
@media (max-width: 435px) {.btn{padding:0.375rem 0.5rem;}}
@media (max-width: 355px) {.btn{padding:0.375rem 0.4rem;}}
div[id="pywebio-scope-board"] .btn {width: 80px; height: 80px;}
.pywebio {min-height:calc(100vh - 50px);}
div[id$="-move-option"] button {color: #bdc6c8; display: inline-flex; align-item: flex-start;
 vertical-align: top; padding: 0px; line-height: 0.75; font-style: italic; font-size: 11px;
 white-space: nowrap;}
"""

PIECE_URL_TEMPLATE = "https://www.chess.com/chess-themes/pieces/neo/150/{piece_color}{piece_type}.png"
PIECE_TYPES = {"Pawn": "p", "Rook": "r", "Knight": "n", "Bishop": "b", "Queen": "q", "King": "k"}

PIECE_URLS: dict[str, tuple[str, ...]] = {}
for piece, piece_type in PIECE_TYPES.items():
    PIECE_URLS[piece] = (
        PIECE_URL_TEMPLATE.format(piece_color="w", piece_type=piece_type),
        PIECE_URL_TEMPLATE.format(piece_color="b", piece_type=piece_type),
    )


@dataclass
class ClientGame:
    game: Game
    options: list[str]
    sessions: List[ThreadBasedSession] = field(default_factory=list)
    colors: dict[str, str] = field(default_factory=dict)
    piece_urls: dict[str, tuple[str, ...]] = field(default_factory=lambda: PIECE_URLS)


@dataclass
class SharedPosition:
    board: Board
    get_result: Callable[[Board], str | None]
    options: list[str]
    piece_urls: dict[str, tuple[str, ...]] = field(default_factory=lambda: PIECE_URLS)


public_games: dict[str, tuple[float, ClientGame]] = {}
client_games: dict[str, ClientGame] = {}
shared_positions: dict[str, SharedPosition] = {}

PS = ParamSpec("PS")
RT = TypeVar("RT")


def for_all_game_sessions(func: Callable[PS, RT]) -> Callable[PS, RT]:
    game_id = session_data.game_id

    def wrapper(*args, **kwargs):
        game = client_games[game_id]
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
    client_game = client_games[session_data.game_id]
    player_index = list(client_game.colors.keys()).index(piece.player.name)
    return client_game.piece_urls[piece.name][player_index]


def move_piece(piece: Piece, move_option: MoveOption):
    if session_data.clicked_position is None:
        return
    session_data.clicked_position = None
    piece.move(move_option)


def show_multiple_move_options(piece: Piece, move_options: List[MoveOption]):
    with popup("Choose an option"):
        for move_option in move_options:
            def on_click(_move_option=deepcopy(move_option)):
                move_piece(piece, _move_option)
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
                    on_click = lambda _move_option=move_option: move_piece(piece, _move_option)
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
                content.style("background-color: #3c93f2")  # #4bb543
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
        if len(client_games[session_data.game_id].sessions) < 2:
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


def share_position():
    board = session_data.game.board.clone()
    get_result = deepcopy(session_data.game._get_result)
    options = client_games[session_data.game_id].options
    piece_urls = client_games[session_data.game_id].piece_urls

    position_id = str(uuid4())
    shared_positions[position_id] = SharedPosition(board, get_result, options, piece_urls)

    run_js("navigator.clipboard.writeText(window.location.href.split('?')[0] + '?position_id=' + position_id);",
           position_id=position_id)
    toast("Position URL copied to clipboard")


def invite():
    game_id = session_data.game_id
    run_js("navigator.clipboard.writeText(window.location.href.split('?')[0] + '?game_id=' + game_id);", game_id=game_id)
    toast("Invite URL copied to clipboard")


def initialize_board():
    board: Board = session_data.game.board
    options = client_games[session_data.game_id].options
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
    client_games[game_id].sessions.append(ThreadBasedSession.get_current_session())
    game = client_games[game_id].game

    session_data.game = game
    session_data.game_id = game_id
    session_data.own_game = False

    put_markdown("""# ChessMaker \n """).style("text-align:center")
    put_button("Copy position URL", onclick=share_position)
    initialize_board()
    put_markdown(
        "[Docs](https://wolfdwyc.github.io/ChessMaker) - [Source](https://github.com/WolfDWyc/ChessMaker)\nMade by WolfDWyc").style(
        "text-align:center")


def new_game(game_factory: Callable[..., Game], options: list[str], mode: str, piece_urls: dict[str, tuple[str, ...]]):
    game: Game = game_factory(**{option: True for option in options})
    game_id = str(uuid4())

    session_data.game = game
    session_data.game_id = game_id

    client_game = ClientGame(game, options, [ThreadBasedSession.get_current_session()], {}, piece_urls)
    colors = ["w", "b"]
    for player in game.board.players:
        client_game.colors[player.name] = colors.pop(0)

    client_games[game_id] = client_game
    if mode == "Multiplayer (Public)":
        public_games[game_id] = (time.time(), client_game)

    session_data.own_game = True
    if mode != "Singleplayer":
        session_data.player = game.board.current_player
    else:
        session_data.player = ""

    game.board.subscribe(AfterMoveEvent, for_all_game_sessions(on_after_move), EventPriority.VERY_LOW + 1)
    game.board.subscribe(AfterTurnChangeEvent, for_all_game_sessions(on_after_turn_change))
    game.subscribe(AfterGameEndEvent, for_all_game_sessions(on_game_end))

    put_markdown("""# ChessMaker \n """).style("text-align:center")
    buttons = [put_button("Copy position URL", onclick=share_position)]
    if mode == "Multiplayer (Private)":
        buttons.append(put_button("Copy invite URL", onclick=invite))
    put_scope("buttons", content=buttons).style("display: flex; justify-content: start; gap: 5px")

    initialize_board()
    put_markdown(
        "[Docs](https://wolfdwyc.github.io/ChessMaker)"
        " - [Source](https://github.com/WolfDWyc/ChessMaker)\nMade by WolfDWyc").style(
        "text-align:center"
    )


def start_pywebio_chess_server(
        game_factory: Callable[..., Game],
        supported_options: List[str] = None,
        piece_urls: dict[str, tuple[str, ...]] = PIECE_URLS,
        remote_access: bool = False,
        port: int = 8000,
        debug: bool = False,
):
    if supported_options is None:
        supported_options = []

    @config(
        title="ChessMaker",
        description="An easily extendible chess implementation designed to support any custom rule or feature.",
        css_style=CSS
    )
    def main():
        games_to_remove = []
        for game_id, (time_created, game) in public_games.items():
            if time.time() - time_created > 5 * 60:
                games_to_remove.append(game_id)
        for game_id in games_to_remove:
            public_games.pop(game_id)

        if get_query("game_id"):
            if get_query("game_id") not in client_games:
                popup("Error", put_error("Game not found"))
            else:
                join_game(get_query("game_id"))
            return

        if get_query("position_id"):
            if get_query("position_id") not in shared_positions:
                popup("Error", put_error("Position not found"))
            else:
                form_result = input_group("New Game", [
                    radio("Mode", ["Singleplayer", "Multiplayer (Private)", "Multiplayer (Public)"], name="mode",
                          value="Singleplayer"),
                    actions("-", [
                        {"label": "Create", "value": "create"},
                    ], name="action"),
                ])
                shared_position = shared_positions[get_query("position_id")]
                new_game(lambda **_: Game(shared_position.board.clone(), deepcopy(shared_position.get_result)),
                         shared_position.options, form_result["mode"], piece_urls)
            return

        form_result = input_group("New Game", [
            radio("Mode", ["Singleplayer", "Multiplayer (Private)", "Multiplayer (Public)"], name="mode",
                  value="Singleplayer"),
            checkbox(
                "Options",
                options=supported_options,
                name="options",
                help_text=f"See details at https://wolfdwyc.github.io/ChessMaker/packaged-variants/"
            ),
            actions("Public Games", [
                {"label": f"Join game: {', '.join(public_game.options) or 'standard'}", "value": game_id}
                for game_id, (_, public_game) in public_games.items()
            ], name="public_games"),
            actions("-", [
                {"label": "Create", "value": "create"},
            ], name="action"),
        ])

        if form_result["public_games"] is not None:
            public_games.pop(form_result["public_games"])
            join_game(form_result["public_games"])
            return

        new_game(game_factory, form_result["options"], form_result["mode"], piece_urls)

    start_server(main, port=port, remote_access=remote_access, debug=debug)


if __name__ == "__main__":
    start_pywebio_chess_server(
        create_game,
        supported_options=["chess960", "knooks", "forced_en_passant", "knight_boosting", "omnipotent_f6_pawn",
                           "siberian_swipe", "il_vaticano", "beta_decay", "la_bastarda", "king_cant_move_to_c2",
                           "vertical_castling", "double_check_to_win", "capture_all_pieces_to_win", "duck_chess"],
        piece_urls=PIECE_URLS |
                   {
                       "Knook": ["https://i.imgur.com/UiWcdEb.png", "https://i.imgur.com/g7xTVts.png"],
                       "Duck": ["https://i.imgur.com/ZZ2WSUq.png", "https://i.imgur.com/ZZ2WSUq.png"]
                   }
    )
