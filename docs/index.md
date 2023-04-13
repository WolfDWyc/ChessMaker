# ChessMaker

An easily extendible chess implementation designed
to support any custom rule or feature.

**Documentation**: [https://wolfdwyc.github.io/ChessMaker](https://wolfdwyc.github.io/ChessMaker)

**Source Code**: [https://github.com/WolfDWyc/ChessMaker](https://wolfdwyc.github.io/ChessMaker)

---

## What is ChessMaker?

ChessMaker is a Python (3.11+) chess implementation that can be extended to support any custom rule or feature.
It allows you to build almost any variant you can think of easily and quickly.

ChessMaker isn't tied to any GUI, but comes with a thin, [pywebio](https://pywebio.readthedocs.io/en/latest/), multiplayer web interface.

It was inspired by [r/AnarchyChess](https://www.reddit.com/r/AnarchyChess/) - and the packaged optional rules are almost all inspired by that subreddit.

These rules are:

* Chess960
* Knooks
* Forced En Passant
* Knight Boosting
* Siberian Swipe
* Il Vaticano
* Beta Decay
* Omnipotent F6 Pawn

## What ChessMaker isn't

* A complete chess server - It doesn't support users, matchmaking, ratings, cheating detection, etc. 
The frontend is very simple and not the focus of the project.
* A chess engine. The design choices are not optimized for speed, and it doesn't provide any analysis or AI.
* A compliant or standard chess implementation. It doesn't support UCI or existing chess GUIs,
because it allows rules that wouldn't be possible with those.

!!! note
    While ChessMaker isn't a chess server, one could be built on top of it, and development of alternative clients to it is welcomed and encouraged.


