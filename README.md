# MiniUCI

This chess GUI is not meant to compete with programs like En Croissant or
Nibbler. This project exists because I had trouble finding a free, open-source,
not web-based, not electron-based chess GUI for interacting with UCI engines.

This project is currently in active development, so if you have any
contributions, don't hesitate to submit a PR.

## Usage

One of the previous versions of this program was written in Python, and there
should be a release available. To run that, simply install all of the packages
listed in the requirements file, then run a python interpreter on the `miniuci`
directory. There are currently no releases of the Haskell rewrite, so you will
have to build from source if you want to check that out.

Since I just recently started the Haskell refactor, not a lot of features are
implemented. It will take a little while to catch up with the Python
implementation since I am rolling my own Chess library, and Haskell just has a
lower development velocity than Python.

Moving pieces works like you'd expect. Press space to highlight the best move,
it may take some time while the engine thinks. Below is a summary of the
keybinds:

- `f`: Flip the board orientation
- `r`: Reset the board to the starting position
- `space`: Highlight the best move
- `left arrow`: Undo the last move

## Configuration

To configure the engine, you can change the settings in the `settings.json`
file. The `engine` key can be set to any UCI compatible engine on your PATH.
The `limit` setting controls how long the engine will search. If the `kind` is
`depth`, it will search for the specified number of plies. If it is `time`, it
will search for the specified number of seconds (not milliseconds).

## Agenda

* [ ] Chess library
* [ ] Rendering board and pieces
