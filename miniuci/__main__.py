import asyncio

import chess.engine
import pygame

import miniuci.config
from miniuci import app, ui
from miniuci.config import Config
from miniuci.ui import blank


def build_ui() -> ui.Root:
    return (
        ui.Builder()
        .with_component(blank.Component((100, 100), pygame.Color(0xFF, 0x00, 0x00)))
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
    pygame.init()


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
