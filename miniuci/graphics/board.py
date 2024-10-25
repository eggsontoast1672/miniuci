from typing import Optional

import chess
from chess import Move, Square
from pygame import Surface

from miniuci.resources import ResourceManager


class Board:
    def __init__(self) -> None:
        self.best_move: Optional[Move] = None
        self.from_square: Optional[Square] = None
        self.orientation = chess.WHITE
        self.manager = ResourceManager()

    def draw(self, board: chess.Board, surface: Surface) -> None:
        self.draw_background(surface)
        self.draw_pieces(board, surface)

    def draw_background(self, surface: Surface) -> None:
        for square in chess.SQUARES:
            pass

    def draw_pieces(self, board: chess.Board, surface: Surface) -> None:
        pass
