from pygame import Surface

from miniuci.settings import ACTIVE_BAR_HEIGHT, ACTIVE_BAR_WIDTH


class ActiveBar:
    ACTIVE_COLOR = "green"
    INACTIVE_COLOR = "red"

    def __init__(self) -> None:
        self.active = False
        self.surface = Surface((ACTIVE_BAR_WIDTH, ACTIVE_BAR_HEIGHT))

    def activate(self) -> None:
        self.active = True

    def deactivate(self) -> None:
        self.active = False

    def draw(self) -> None:
        if self.active:
            self.surface.fill(self.ACTIVE_COLOR)
        else:
            self.surface.fill(self.INACTIVE_COLOR)
