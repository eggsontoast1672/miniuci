from miniuci import ui


class Component(ui.Component):
    def get_size(self) -> tuple[int, int]:
        return super().get_size()

    def render(self, state: ui.State) -> Surface:
        return super().render(state)
