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

- `space`: Highlight the best move
- `left arrow`: Undo the last move

## Agenda

* Organize code
* Async child process
* Promotion mechanic
* Eval bar
* Continuous eval, info line parsing
* Engine active indicator
* Best move arrows
* Sound effects
* Image anti-aliasing
