import math
from typing import Optional

import chess
import pygame
from chess import Square
from pygame import Rect, Surface, Vector2

from miniuci import ui
from miniuci.resources import ResourceManager

CELL_SIZE = 80

LIGHT_SQUARE_COLOR = pygame.Color(0xF0, 0xD9, 0xB5)
DARK_SQUARE_COLOR = pygame.Color(0xB5, 0x88, 0x63)
FROM_SQUARE_COLOR = pygame.Color(0xFF, 0x00, 0x00)
BEST_SQUARE_COLOR = pygame.Color(0xFF, 0xFF, 0x00)


class Component(ui.Component):
    def __init__(self) -> None:
        super().__init__()
        self.from_square: Optional[Square] = None
        self.manager = ResourceManager()
        self.surface = Surface((CELL_SIZE * 8, CELL_SIZE * 8))

    def get_size(self) -> tuple[int, int]:
        return self.surface.get_size()

    def get_square_color(self, square: Square, state: ui.State) -> pygame.Color:
        pos = self.get_square_pos(square, state)
        if self.is_square_best_move(square, state):
            return BEST_SQUARE_COLOR
        elif square == self.from_square:
            return FROM_SQUARE_COLOR
        elif (pos.x + pos.y) % 2 == 0:
            return LIGHT_SQUARE_COLOR
        else:
            return DARK_SQUARE_COLOR

    def get_square_pos(self, square: Square, state: ui.State) -> Vector2:
        file = chess.square_file(square)
        rank = chess.square_rank(square)
        if state.app.orientation:
            return Vector2(file, 7 - rank)
        else:
            return Vector2(7 - file, rank)

    def get_square_under_mouse(self, white: bool) -> Square:
        file = math.floor(self.mouse_pos[0] / CELL_SIZE)
        rank = math.floor(self.mouse_pos[1] / CELL_SIZE)

        # TODO: This won't work
        if white:
            return chess.square(file, rank)
        else:
            return chess.square(file, rank)

    @staticmethod
    def is_square_best_move(square: Square, state: ui.State) -> bool:
        if state.app.best_move is None:
            return False
        is_from_square = square == state.app.best_move.from_square
        is_to_square = square == state.app.best_move.to_square
        return is_from_square or is_to_square

    def on_mouse_button_down(self, state: ui.State) -> None:
        square = self.get_square_under_mouse()

    def render(self, state: ui.State) -> Surface:
        self.render_background(state)
        self.render_pieces(state)
        return self.surface

    def render_background(self, state: ui.State) -> None:
        for square in chess.SQUARES:
            pos = self.get_square_pos(square, state)
            color = self.get_square_color(square, state)
            rect = Rect(pos * CELL_SIZE, (CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(self.surface, color, rect)

    def render_pieces(self, state: ui.State) -> None:
        held_piece = None

        for color in chess.COLORS:
            for piece in chess.PIECE_TYPES:
                squares = state.app.board.pieces(piece, color)
                image = self.manager.get(piece, color)
                for square in squares:
                    if square == self.from_square:
                        held_piece = image
                        continue
                    elif state.app.orientation:
                        pos = Vector2(
                            chess.square_file(square), 7 - chess.square_rank(square)
                        )
                    else:
                        pos = Vector2(
                            7 - chess.square_file(square), chess.square_rank(square)
                        )
                    self.surface.blit(image, pos * CELL_SIZE)
        if held_piece is not None:
            self.surface.blit(
                held_piece,
                (self.mouse_pos[0] - CELL_SIZE / 2, self.mouse_pos[1] - CELL_SIZE / 2),
            )
