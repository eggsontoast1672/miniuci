from typing import Optional

import chess
import pygame
from chess import Move, Square
from pygame import Surface, Vector2

from miniuci.resources import ResourceManager
from miniuci.settings import (
    BOARD_BEST_SQUARE_COLOR,
    BOARD_DARK_SQUARE_COLOR,
    BOARD_FROM_SQUARE_COLOR,
    BOARD_LIGHT_SQUARE_COLOR,
    BOARD_SIZE,
    BOARD_X,
    CELL_SIZE,
)


class Board:
    def __init__(self) -> None:
        self.best_move: Optional[Move] = None
        self.from_square: Optional[Square] = None
        self.manager = ResourceManager()
        self.surface = Surface((BOARD_SIZE, BOARD_SIZE))

    def draw(self, board: chess.Board, orientation: chess.Color) -> None:
        self.draw_background(orientation)
        self.draw_pieces(board, orientation)

    def draw_background(self, orientation: chess.Color) -> None:
        for square in chess.SQUARES:
            pos = self.get_square_pos(square, orientation)
            color = self.get_square_color(square, orientation)
            rect = pygame.Rect(pos * CELL_SIZE, (CELL_SIZE, CELL_SIZE))

            pygame.draw.rect(self.surface, color, rect)

    def draw_pieces(self, board: chess.Board, orientation: chess.Color) -> None:
        held_piece = None

        for color in chess.COLORS:
            for piece in chess.PIECE_TYPES:
                squares = board.pieces(piece, color)
                image = self.manager.get(piece, color)
                for square in squares:
                    if square == self.from_square:
                        held_piece = image
                        continue
                    elif orientation:
                        pos = Vector2(
                            chess.square_file(square),
                            7 - chess.square_rank(square),
                        )
                    else:
                        pos = Vector2(
                            7 - chess.square_file(square),
                            chess.square_rank(square),
                        )
                    self.surface.blit(image, pos * CELL_SIZE)

        # If we are holding a piece, we want it to be drawn above all of the
        # other pieces.
        if held_piece is not None:
            x, y = pygame.mouse.get_pos()
            self.surface.blit(
                held_piece, (x - BOARD_X - CELL_SIZE / 2, y - CELL_SIZE / 2)
            )

    def get_from_square(self) -> Optional[Square]:
        return self.from_square

    def get_square_color(
        self, square: Square, orientation: chess.Color
    ) -> pygame.Color:
        pos = self.get_square_pos(square, orientation)
        if self.is_square_best_move(square):
            return BOARD_BEST_SQUARE_COLOR
        elif square == self.from_square:
            return BOARD_FROM_SQUARE_COLOR
        elif (pos.x + pos.y) % 2 == 0:
            return BOARD_LIGHT_SQUARE_COLOR
        else:
            return BOARD_DARK_SQUARE_COLOR

    def get_square_pos(self, square: Square, orientation: chess.Color) -> Vector2:
        file = chess.square_file(square)
        rank = chess.square_rank(square)
        if orientation:
            return Vector2(file, 7 - rank)
        else:
            return Vector2(7 - file, rank)

    def is_holding_piece(self) -> bool:
        return self.from_square is not None

    def is_square_best_move(self, square: Square) -> bool:
        if self.best_move is None:
            return False
        is_from_square = square == self.best_move.from_square
        is_to_square = square == self.best_move.to_square
        return is_from_square or is_to_square

    def reset_best_move(self) -> None:
        self.best_move = None

    def reset_from_square(self) -> None:
        self.from_square = None

    def set_best_move(self, move: Move) -> None:
        self.best_move = move

    def set_from_square(self, square: Square) -> None:
        self.from_square = square
