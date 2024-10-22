import chess
import pygame

from miniuci.settings import CELL_SIZE


class ResourceManager:
    def __init__(self) -> None:
        self.cache: dict[str, pygame.Surface] = {}

    def get(self, piece_type: chess.PieceType, color: chess.Color) -> pygame.Surface:
        piece_type_str = chess.PIECE_NAMES[piece_type]
        color_str = chess.COLOR_NAMES[color]
        name = f"{color_str}-{piece_type_str}"
        if name not in self.cache:
            image = pygame.image.load(f"assets/{name}.png")
            self.cache[name] = pygame.transform.scale(image, (CELL_SIZE, CELL_SIZE))
        return self.cache[name]
