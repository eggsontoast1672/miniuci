import pygame
from pygame import Surface

from miniuci import ui


class Component(ui.Component):
    def __init__(self, size: tuple[int, int], color: pygame.Color) -> None:
        self.size = size
        self.color = color

    def get_size(self) -> tuple[int, int]:
        return self.size

    def render(self, state: ui.State) -> Surface:
        surface = Surface(self.size)
        surface.fill(self.color)
        return surface
