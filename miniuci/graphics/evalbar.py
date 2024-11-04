from typing import Optional

import chess
import pygame
from chess.engine import Cp, PovScore
from pygame import Surface

from miniuci.settings import CELL_SIZE, EVAL_BAR_HEIGHT, EVAL_BAR_WIDTH


class EvalBar:
    def __init__(self) -> None:
        self.score = PovScore(Cp(0), chess.WHITE)
        self.surface = Surface((EVAL_BAR_WIDTH, EVAL_BAR_HEIGHT))

    def draw(self, orientation: chess.Color) -> None:
        score = self.score.pov(not orientation).score()
        height = self.get_height(score)
        if orientation:
            self.surface.fill("white")
            pygame.draw.rect(self.surface, "black", (0, 0, EVAL_BAR_WIDTH, height))
        else:
            self.surface.fill("black")
            pygame.draw.rect(self.surface, "white", (0, 0, EVAL_BAR_WIDTH, height))

    @staticmethod
    def get_height(score: Optional[int]) -> float:
        if score is None:
            return 0
        halfway = EVAL_BAR_HEIGHT * 0.5
        offset = score * 0.01 * CELL_SIZE * 0.5
        return pygame.math.clamp(
            halfway + offset,
            CELL_SIZE * 0.5,
            EVAL_BAR_HEIGHT - CELL_SIZE * 0.5,
        )

    def set_score(self, score: PovScore) -> None:
        self.score = score
