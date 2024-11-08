from typing import Optional
import pygame
from pygame import Surface

from miniuci import ui


class Component(ui.Component):
    def __init__(self) -> None:
        super().__init__()
        self.surface = Surface((20, 640))

    def get_height(self, score: Optional[int]) -> float:
        CELL_SIZE = 80

        if score is None:
            return 0
        halfway = self.surface.get_height() * 0.5
        offset = score * 0.01 * CELL_SIZE * 0.5
        return pygame.math.clamp(
            halfway + offset,
            CELL_SIZE * 0.5,
            self.surface.get_height() - CELL_SIZE * 0.5,
        )

    def get_size(self) -> tuple[int, int]:
        return self.surface.get_size()

    def render(self, state: ui.State) -> Surface:
        score = state.app.score.pov(not state.app.orientation).score()
        height = self.get_height(score)
        if state.app.orientation:
            self.surface.fill("white")
            pygame.draw.rect(
                self.surface, "black", (0, 0, self.surface.get_width(), height)
            )
        else:
            self.surface.fill("black")
            pygame.draw.rect(
                self.surface, "white", (0, 0, self.surface.get_width(), height)
            )
        return self.surface
