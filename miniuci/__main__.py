import asyncio

import chess.engine
import pygame
from chess.engine import Cp, Limit, PovScore
from pygame.math import Vector2

from miniuci.clock import AsyncClock
import miniuci.config
from miniuci import app, ui
from miniuci.config import Config
from miniuci.ui import board, evalbar, status


def build_ui() -> ui.Root:
    return (
        ui.Builder()
        .with_component(status.Component())
        .with_component(evalbar.Component())
        .with_component(board.Component())
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


async def display_best_move(state: app.State) -> None:
    state.thinking = True
    with await state.engine.analysis(state.board, limit=Limit(depth=14)) as analysis:
        async for info in analysis:
            print(info)

            score = info.get("score")
            if score is not None:
                state.score = score

            pv = info.get("pv")
            if pv is not None:
                state.best_move = pv[0]
    state.thinking = False


async def start_test_ui(command: str, root: ui.Root) -> None:
    screen = pygame.display.set_mode(root.get_size())
    clock = AsyncClock()

    transport, engine = await chess.engine.popen_uci(command)
    app_state = app.State(engine)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_f:
                        app_state.orientation = not app_state.orientation
                    case pygame.K_r:
                        app_state.board.reset()
                        app_state.engine.send_line("stop")
                        app_state.thinking = False
                        app_state.score = PovScore(Cp(0), chess.WHITE)
                    case pygame.K_LEFT:
                        try:
                            app_state.board.pop()
                        except IndexError:
                            pass
                    case pygame.K_SPACE:
                        asyncio.create_task(display_best_move(app_state))

        state = ui.State(app.State(engine), Vector2(0, 0))
        screen.blit(root.render(state), (0, 0))
        pygame.display.flip()
        await clock.tick(60)


async def main() -> None:
    config = miniuci.config.get_config()
    dump_config(config)

    pygame.init()

    ######
    # UI #
    ######
    root = build_ui()
    await start_test_ui(config.engine, root)
    return

    await app.App(config, engine).run()


if __name__ == "__main__":
    asyncio.run(main())
