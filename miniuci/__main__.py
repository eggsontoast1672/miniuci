import asyncio

import chess.engine
import pygame

import miniuci.config
from miniuci import ui
from miniuci.config import Config
from miniuci.ui import blank


def build_ui() -> ui.Root:
    return (
        ui.Builder()
        .with_component(blank.Component((100, 200), pygame.Color(0xFF, 0x00, 0x00)))
        .with_component(blank.Component((100, 100), pygame.Color(0x00, 0xFF, 0x00)))
        .with_component(blank.Component((100, 100), pygame.Color(0x00, 0xFF, 0xFF)))
        .build()
    )


def dump_config(config: Config) -> None:
    print(f"Engine: {config.engine}")
    print("Limit: ", end="")
    if config.limit.depth is not None:
        print(f"{config.limit.depth} plies")
    elif config.limit.time is not None:
        print(f"{config.limit.time} seconds")
    else:
        assert False, "unreachable"


def start_test_ui(root: ui.Root) -> None:
    screen = pygame.display.set_mode(root.get_size())
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.blit(root.render(0), (0, 0))
        pygame.display.flip()
        clock.tick(60)


async def main() -> None:
    config = miniuci.config.get_config()
    dump_config(config)

    pygame.init()

    ######
    # UI #
    ######
    root = build_ui()
    start_test_ui(root)
    return

    transport, engine = await chess.engine.popen_uci(config.engine)
    await app.App(config, engine).run()


if __name__ == "__main__":
    asyncio.run(main())
