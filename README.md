# MiniUCI

This chess GUI is not meant to compete with programs like En Croissant or
Nibbler. This project exists because I had trouble finding a free, open-source,
not web-based, not electron-based chess GUI for interacting with UCI engines.

This project is currently in active development, so if you have any
contributions, don't hesitate to submit a PR.

## Usage

Simply install all of the packages listed in the requirements file, then run a
python interpreter on the `miniuci` directory. Moving pieces works like you'd
expect. Press space to highlight the best move, it may take some time while the
engine thinks. Below is a summary of the keybinds:

- `f`: Flip the board orientation
- `r`: Reset the board to the starting position
- `space`: Highlight the best move
- `left arrow`: Undo the last move

## Configuration

To configure the engine, you can change the settings in the
`settings.json` file. The `engine` key can be set to any UCI
compatible engine on your PATH. The `limit` setting controls how
long the engine will search. If the `kind` is `depth`, it will
search for the specified number of plies. If it is `time`, it will
search for the specified number of seconds (not milliseconds).

## Agenda

* Async child process
    * Continuous eval, info line parsing
* Organize code
    * Split up board and eval bar modules
* Improve UI
    * Best move arrows
    * Print material count
    * Engine active indicator
    * Image anti-aliasing
    * Check indicator
    * Better selected piece visuals
* Promotion mechanic
* Sound effects

## Known Bugs

* Eval bar doesn't reset after full board reset
