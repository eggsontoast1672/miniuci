import math
from typing import Optional

import chess
import pygame
from chess import Move, Square
from chess.engine import PovScore
from pygame import Surface

from miniuci.graphics.activebar import ActiveBar
from miniuci.graphics.evalbar import EvalBar
from miniuci.graphics.board import Board
from miniuci.settings import (
    ACTIVE_BAR_WIDTH,
    ACTIVE_BAR_X,
    ACTIVE_BAR_Y,
    BOARD_X,
    BOARD_Y,
    CELL_SIZE,
    EVAL_BAR_WIDTH,
    EVAL_BAR_X,
    EVAL_BAR_Y,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
)


class Interface:
    def __init__(self) -> None:
        self.activebar = ActiveBar()
        self.evalbar = EvalBar()
        self.board = Board()
        self.orientation = chess.WHITE
        self.surface = Surface((WINDOW_WIDTH, WINDOW_HEIGHT))

    def activate(self) -> None:
        self.activebar.activate()

    def deactivate(self) -> None:
        self.activebar.deactivate()

    def draw(self, board: chess.Board) -> None:
        self.activebar.draw()
        self.evalbar.draw(self.orientation)
        self.board.draw(board, self.orientation)

        self.surface.blit(self.activebar.surface, (ACTIVE_BAR_X, ACTIVE_BAR_Y))
        self.surface.blit(self.evalbar.surface, (EVAL_BAR_X, EVAL_BAR_Y))
        self.surface.blit(self.board.surface, (BOARD_X, BOARD_Y))

    def flip_orientation(self) -> None:
        self.orientation = not self.orientation

    def get_from_square(self) -> Optional[Square]:
        return self.board.get_from_square()

    def get_square_under_mouse(self) -> Square:
        x, y = pygame.mouse.get_pos()
        file = math.floor((x - BOARD_X) / CELL_SIZE)
        rank = math.floor(y / CELL_SIZE)
        if self.orientation:
            return chess.square(file, 7 - rank)
        else:
            return chess.square(7 - file, rank)

    def is_holding_piece(self) -> bool:
        return self.board.is_holding_piece()

    def reset(self) -> None:
        pass

    def reset_best_move(self) -> None:
        self.board.reset_best_move()

    def reset_from_square(self) -> None:
        self.board.reset_from_square()

    def set_best_move(self, move: Move) -> None:
        self.board.set_best_move(move)

    def set_from_square(self, square: Square) -> None:
        self.board.set_from_square(square)

    def set_score(self, score: PovScore) -> None:
        self.evalbar.set_score(score)
