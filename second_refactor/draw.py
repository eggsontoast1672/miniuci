import itertools
from typing import Optional

import chess
import pygame
from chess import Board, Square
from pygame import Rect, Surface, Vector2


def get_cell_size(surface: Surface) -> Vector2:
    width, height = surface.get_size()
    return Vector2(width / 8, height / 8)


asset_cache = {}


def get_asset(color: chess.Color, piece: chess.PieceType) -> Surface:
    name = f"assets/{chess.COLOR_NAMES[color]}-{chess.PIECE_NAMES[piece]}.png"
    if name not in asset_cache:
        asset_cache[name] = pygame.image.load(name)
    return asset_cache[name]


def board(surface: Surface) -> None:
    cell_size = get_cell_size(surface)
    for x, y in itertools.product(range(8), repeat=2):
        if (x + y) % 2 == 0:
            color = pygame.Color(0xF0D9B5FF)
        else:
            color = pygame.Color(0xB58863FF)
        pygame.draw.rect(surface, color, Rect(
            (x * cell_size.x, y * cell_size.y),
            cell_size))


def pieces(surface: Surface, board: Board, held: Optional[Square]) -> None:
    cell_size = get_cell_size(surface)
    for color, piece in itertools.product(chess.COLORS, chess.PIECE_TYPES):
        asset = pygame.transform.scale(get_asset(color, piece), cell_size)
        for square in board.pieces(piece, color):
            surface.blit(asset, Vector2(
                (7 - chess.square_file(square)) * cell_size.x,
                chess.square_rank(square) * cell_size.y))

