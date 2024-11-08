from pygame import Surface

from miniuci import ui

THINKING_COLOR = "green"
NEUTRAL_COLOR = "red"


class Component(ui.Component):
    def __init__(self) -> None:
        super().__init__()
        self.surface = Surface((10, 10))

    def get_size(self) -> tuple[int, int]:
        return self.surface.get_size()

    def render(self, state: ui.State) -> Surface:
        if state.app.thinking:
            self.surface.fill(THINKING_COLOR)
        else:
            self.surface.fill(NEUTRAL_COLOR)
        return self.surface
