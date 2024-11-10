import asyncio

import chess.engine
import pygame

from miniuci_refactor import ui
from miniuci_refactor.clock import AsyncClock


async def main() -> None:
    pygame.init()

    screen = pygame.display.set_mode((640, 640))
    transport, engine = await chess.engine.popen_uci("stockfish")
    root = ui.RootComponent(engine)
    clock = AsyncClock()
    running = True

    while running:
        for event in pygame.event.get():
            match event.type:
                case pygame.KEYDOWN:
                    root.on_key_press(event)
                case pygame.MOUSEBUTTONDOWN:
                    root.on_mouse_down()
                case pygame.QUIT:
                    running = False

        screen.blit(root.render(), (0, 0))
        pygame.display.flip()
        await clock.tick(60)


if __name__ == "__main__":
    asyncio.run(main())
