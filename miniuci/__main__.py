import asyncio

import chess.engine
import pygame

import miniuci.config
from miniuci import app
from miniuci.config import Config


def dump_config(config: Config) -> None:
    print(f"Engine: {config.engine}")
    print("Limit: ", end="")
    if config.limit.depth is not None:
        print(f"{config.limit.depth} plies")
    elif config.limit.time is not None:
        print(f"{config.limit.time} seconds")
    else:
        assert False, "unreachable"


async def main() -> None:
    config = miniuci.config.get_config()
    dump_config(config)

    pygame.init()

    transport, engine = await chess.engine.popen_uci(config.engine)
    await app.App(config, engine).run()


if __name__ == "__main__":
    asyncio.run(main())
