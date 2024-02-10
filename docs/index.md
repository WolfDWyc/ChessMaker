# ChessMaker

An easily extendible chess implementation designed
to support any custom rule or feature.

<span style="font-size:x-large;"><b>
Play: [https://chessmaker.fly.dev](https://chessmaker.fly.dev/)
</b></span>

**Documentation**: [https://wolfdwyc.github.io/ChessMaker](https://wolfdwyc.github.io/ChessMaker)

**Source Code**: [https://github.com/WolfDWyc/ChessMaker](https://github.com/WolfDWyc/ChessMaker)

---

## What is ChessMaker?

ChessMaker is a Python (3.11+) chess implementation that can be extended to support any custom rule or feature.
It allows you to build almost any variant you can think of easily and quickly.

It was inspired by [r/AnarchyChess](https://www.reddit.com/r/AnarchyChess/) - and the packaged optional rules are almost all inspired by that subreddit.

ChessMaker isn't tied to any GUI, but comes with a thin, [pywebio](https://pywebio.readthedocs.io/en/latest/), multiplayer web interface.
The web interface supports choosing from the packaged rules, singleplayer (vs Yourself), and multiplayer
(vs a friend or random opponent). It also supports saving and loading games - which can be shared with others
and be used as puzzles.

The packaged rules are:

* Chess960
* Knooks
* Forced En Passant
* Knight Boosting
* Siberian Swipe
* Il Vaticano
* Beta Decay
* La Bastarda
* Omnipotent F6 Pawn
* King Cant Move to C2
* Vertical Castling
* Double Check to Win
* Capture All Pieces to Win
* Duck Chess

Contributions of new variants or anything else you'd like to see in the project are welcome!

## What ChessMaker isn't

* A complete chess server - It currently doesn't support users, matchmaking, ratings, cheating detection,
and is very thin. The frontend is very simple and currently not the focus of the project.
* A chess engine - The design choices are not optimized for speed, and it doesn't provide any analysis or AI.
* A compliant or standard chess implementation - It doesn't support UCI or existing chess GUIs,
because it allows rules that wouldn't be possible with those.

!!! note
    While ChessMaker isn't a chess server, one could be built on top of it, and development of alternative clients to it is welcomed and encouraged.
    If this project gets enough interest, a more complete server might be added.


