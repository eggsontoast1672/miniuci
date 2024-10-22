import chess
import math
import pygame
from typing import Optional

from miniuci.engine import Evaluation, EvaluationKind
from miniuci.resources import ResourceManager
from miniuci.settings import (
    CELL_SIZE,
    DARK_SQUARE_COLOR,
    EVAL_BAR_HEIGHT,
    EVAL_BAR_WIDTH,
    LIGHT_SQUARE_COLOR,
)


class Board:
    def __init__(self) -> None:
        self.best_move: Optional[chess.Move] = None
        self.eval_bar_height = 320  # TODO: Dynamic eval bar
        self.from_square: Optional[chess.Square] = None
        self.orientation = chess.WHITE
        self.resource_manager = ResourceManager()

    def clear_best_move(self) -> None:
        self.best_move = None

    def clear_from_square(self) -> None:
        self.from_square = None

    def display_best_move(self, move: chess.Move) -> None:
        self.best_move = move

    def draw(self, board: chess.Board, surface: pygame.Surface) -> None:
        self.draw_background(surface)
        self.draw_pieces(board, surface)
        self.draw_eval_bar(surface)

    def draw_background(self, surface: pygame.Surface) -> None:
        for square in chess.SQUARES:
            pos = self.get_square_position(square)
            color = self.get_square_color(square)
            rect = pygame.Rect(
                pos * CELL_SIZE + pygame.Vector2(EVAL_BAR_WIDTH, 0),
                (CELL_SIZE, CELL_SIZE),
            )
            pygame.draw.rect(surface, color, rect)

    def draw_eval_bar(self, surface: pygame.Surface) -> None:
        if self.orientation == chess.BLACK:
            pygame.draw.rect(surface, "black", (0, 0, EVAL_BAR_WIDTH, EVAL_BAR_HEIGHT))
            pygame.draw.rect(
                surface, "white", (0, 0, EVAL_BAR_WIDTH, self.eval_bar_height)
            )
        else:
            pygame.draw.rect(surface, "white", (0, 0, EVAL_BAR_WIDTH, EVAL_BAR_HEIGHT))
            pygame.draw.rect(
                surface,
                "black",
                (0, 0, EVAL_BAR_WIDTH, EVAL_BAR_HEIGHT - self.eval_bar_height),
            )

    def draw_pieces(self, board: chess.Board, surface: pygame.Surface) -> None:
        defer_image = None
        for color in chess.COLORS:
            for piece in chess.PIECE_TYPES:
                squares = board.pieces(piece, color)
                image = self.resource_manager.get(piece, color)
                for square in squares:
                    # If source_square is not None, we must be holding a piece. If
                    # we are holding the piece on this square, draw it at the mouse
                    # cursor's position.
                    if square == self.from_square:
                        defer_image = image
                        continue
                    elif self.orientation == chess.BLACK:
                        x = 7 - chess.square_file(square)
                        y = chess.square_rank(square)
                    else:
                        x = chess.square_file(square)
                        y = 7 - chess.square_rank(square)
                    surface.blit(image, (x * CELL_SIZE + EVAL_BAR_WIDTH, y * CELL_SIZE))
        if defer_image is not None:
            mouse_pos = pygame.mouse.get_pos()
            x = mouse_pos[0] - CELL_SIZE / 2
            y = mouse_pos[1] - CELL_SIZE / 2
            surface.blit(defer_image, (x, y))

    def flip_orientation(self) -> None:
        self.orientation = not self.orientation

    def get_from_square(self) -> Optional[chess.Square]:
        return self.from_square

    def get_square_under_mouse(self) -> chess.Square:
        mouse_pos = pygame.mouse.get_pos()
        file = math.floor((mouse_pos[0] - EVAL_BAR_WIDTH) / CELL_SIZE)
        rank = math.floor((mouse_pos[1] - EVAL_BAR_WIDTH) / CELL_SIZE)
        if self.orientation == chess.BLACK:
            return chess.square(7 - file, rank)
        else:
            return chess.square(file, 7 - rank)

    def get_square_color(self, square: chess.Square) -> pygame.Color:
        pos = self.get_square_position(square)
        if self.is_best_move_square(square):
            return pygame.Color(0xFF, 0xFF, 0x00)
        elif square == self.from_square:
            return pygame.Color(0xFF, 0x00, 0x00)
        elif (pos.x + pos.y) % 2 == 0:
            return LIGHT_SQUARE_COLOR
        else:
            return DARK_SQUARE_COLOR

    def get_square_position(self, square: chess.Square) -> pygame.Vector2:
        file = chess.square_file(square)
        rank = chess.square_rank(square)
        if self.orientation == chess.BLACK:
            return pygame.Vector2(7 - file, rank)
        else:
            return pygame.Vector2(file, 7 - rank)

    def is_best_move_square(self, square: chess.Square) -> bool:
        if self.best_move is None:
            return False
        return square in (self.best_move.from_square, self.best_move.to_square)

    def is_holding_piece(self) -> bool:
        return self.from_square is not None

    def set_eval_bar_height(self, eval_score: Evaluation) -> None:
        match eval_score.kind:
            case EvaluationKind.CENTIPAWN:
                pass
            case EvaluationKind.MATE:
                if self.orientation == chess.BLACK:
                    pass
                else:
                    pass

    def set_from_square(self, square: chess.Square) -> None:
        self.from_square = square
