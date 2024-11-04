import abc
from abc import ABC
from typing import Any, Self

from pygame import Surface


class Component(ABC):
    @abc.abstractmethod
    def get_size(self) -> tuple[int, int]:
        pass

    @abc.abstractmethod
    def render(self, state: Any) -> Surface:
        pass


class Root:
    def __init__(self, components: list[Component]) -> None:
        self.components = components

    def get_size(self) -> tuple[int, int]:
        total_width, total_height = 0, 0
        for component in self.components:
            width, height = component.get_size()
            total_width += width
            total_height += height
        return total_width, total_height


class Builder:
    def __init__(self) -> None:
        self.components = []

    def with_component(self, component: Component) -> Self:
        self.components.append(component)
        return self

    def build(self) -> Root:
        assert False, "todo"
