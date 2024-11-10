import asyncio
from typing import Optional

import pygame


class AsyncClock:
    def __init__(self) -> None:
        self.ticks: Optional[int] = None

    async def tick(self, fps: int) -> None:
        if self.ticks is None:
            self.ticks = pygame.time.get_ticks()
            return

        # 60 frames = 1 second => 1 frame = 1/60 seconds
        frame_time_seconds = (pygame.time.get_ticks() - self.ticks) / 1000
        target_time_seconds = 1 / fps
        if frame_time_seconds < target_time_seconds:
            await asyncio.sleep(target_time_seconds - frame_time_seconds)

        # Make sure to update it for next frame
        self.ticks = pygame.time.get_ticks()
