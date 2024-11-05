from typing import Any

from pygame import Surface

from miniuci import ui

THINKING_COLOR = "green"
NEUTRAL_COLOR = "red"


class Component(ui.Component):
    def __init__(self) -> None:
        self.surface = Surface((10, 10))

    def get_size(self) -> tuple[int, int]:
        return self.surface.get_size()

    def render(self, state: Any) -> Surface:
        if state.engine_is_thinking:
            self.surface.fill(THINKING_COLOR)
        else:
            self.surface.fill(NEUTRAL_COLOR)
        return self.surface
