import abc
from abc import ABC
from typing import Any, Self

from pygame import Surface, Vector2

from miniuci import app


class State:
    def __init__(self, app_state: app.State, mouse: Vector2) -> None:
        self.app = app_state
        self.mouse = mouse


class Component(ABC):
    def __init__(self) -> None:
        self.mouse_pos = (0, 0)

    @abc.abstractmethod
    def get_size(self) -> tuple[int, int]:
        pass

    @abc.abstractmethod
    def render(self, state: State) -> Surface:
        pass


class Root:
    def __init__(self, components: list[Component]) -> None:
        self.components = components

    def get_size(self) -> tuple[int, int]:
        total_width, max_height = 0, 0
        for component in self.components:
            width, height = component.get_size()
            total_width += width
            max_height = max(max_height, height)
        return total_width, max_height

    def render(self, state: Any) -> Surface:
        # TODO: Store surface so we don't have to recalculate the size every
        # single damn time
        surface = Surface(self.get_size())
        position = 0
        for component in self.components:
            rendered = component.render(state)
            surface.blit(rendered, (position, 0))
            position += component.get_size()[0]
        return surface


class Builder:
    def __init__(self) -> None:
        self.components = []

    def with_component(self, component: Component) -> Self:
        self.components.append(component)
        return self

    def build(self) -> Root:
        return Root(self.components)
