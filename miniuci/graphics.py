import math
from typing import Optional

import chess
import pygame

import assets
from engine import Engine
from settings import CELL_SIZE


class Board:
    LIGHT_SQUARE_COLOR = pygame.Color(0xF0, 0xD9, 0xB5)
    DARK_SQUARE_COLOR = pygame.Color(0xB5, 0x88, 0x63)

    def __init__(
        self, board: chess.Board, engine: Engine, surface: pygame.Surface
    ) -> None:
        self.asset_manager = assets.AssetManager()
        self.best_move: Optional[chess.Move] = None
        self.board = board
        self.engine = engine
        self.orientation = chess.WHITE
        self.surface = surface
        self.source_square: Optional[chess.Square] = None

    def display_best_move(self) -> None:
        if self.board.is_checkmate():
            print("checkmate")
            return
        position = self.board.fen()
        self.engine.load_position(position)
        move = self.engine.get_best_move()
        self.best_move = chess.Move.from_uci(move)

    def draw(self) -> None:
        """
        Draw the entire board including background, pieces, and highlighted
        squares.
        """
        self.draw_background()
        if self.source_square is None:
            self.draw_pieces(starting_with=chess.WHITE)
            return
        piece = self.board.piece_at(self.source_square)
        if piece is not None and piece.color == chess.WHITE:
            self.draw_pieces(starting_with=chess.BLACK)
        else:
            self.draw_pieces(starting_with=chess.WHITE)

    def draw_background(self) -> None:
        """
        Draw the light and dark squares of the board behind the pieces.
        """
        for square in chess.SQUARES:
            # ???
            if self.orientation == chess.BLACK:
                x = 7 - chess.square_file(square)
                y = chess.square_rank(square)
            else:
                x = chess.square_file(square)
                y = 7 - chess.square_rank(square)

            if self.best_move is not None and (
                square == self.best_move.from_square
                or square == self.best_move.to_square
            ):
                color = pygame.Color(0xFF, 0xFF, 0x00)
            elif square == self.source_square:
                color = pygame.Color(0xFF, 0x00, 0x00)
            elif (x + y) % 2 == 0:
                color = Board.LIGHT_SQUARE_COLOR
            else:
                color = Board.DARK_SQUARE_COLOR

            pygame.draw.rect(
                self.surface,
                color,
                (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE),
            )

    def draw_pieces(self, *, starting_with: chess.Color) -> None:
        """
        Draw all of the pieces on the board that have the specified color.
        """
        for color in sorted(chess.COLORS, reverse=starting_with == chess.WHITE):
            for piece in chess.PIECE_TYPES:
                squares = self.board.pieces(piece, color)
                image = self.asset_manager.get(piece, color)
                for square in squares:
                    # If source_square is not None, we must be holding a piece. If
                    # we are holding the piece on this square, draw it at the mouse
                    # cursor's position.
                    if square == self.source_square:
                        mouse_pos = pygame.mouse.get_pos()
                        x = mouse_pos[0] - CELL_SIZE / 2
                        y = mouse_pos[1] - CELL_SIZE / 2
                    elif self.orientation == chess.BLACK:
                        x = (7 - chess.square_file(square)) * CELL_SIZE
                        y = chess.square_rank(square) * CELL_SIZE
                    else:
                        x = chess.square_file(square) * CELL_SIZE
                        y = (7 - chess.square_rank(square)) * CELL_SIZE
                    self.surface.blit(image, (x, y))

    def drop_piece_at(self, square: chess.Square) -> None:
        """Place the piece that is currently being held at the target square."""
        assert self.source_square is not None
        move = chess.Move(self.source_square, square)
        if self.is_promotion(move):
            move.promotion = chess.QUEEN
        if self.board.is_legal(move):
            self.board.push(move)
            self.best_move = None
        self.source_square = None

    def flip_orientation(self) -> None:
        """
        Flip the orientation of the board. If it was white's perspective before,
        change it to black's and vice versa.
        """
        self.orientation = not self.orientation

    def get_square(self, mouse_pos: tuple[int, int]) -> chess.Square:
        """
        Given a mouse position in screen space coordinates, calculate which
        square on the chess board is under the mouse at that position
        """
        file = math.floor(mouse_pos[0] / CELL_SIZE)
        rank = math.floor(mouse_pos[1] / CELL_SIZE)
        if self.orientation == chess.BLACK:
            return chess.square(7 - file, rank)
        else:
            return chess.square(file, 7 - rank)

    def is_holding_piece(self) -> bool:
        """Returns true if a piece is now being held, false otherwise"""
        return self.source_square is not None

    def is_promotion(self, move: chess.Move) -> bool:
        """Returns true if the move would be a promotion, false otherwise."""
        piece = self.board.piece_at(move.from_square)
        rank = chess.square_rank(move.to_square)
        assert piece is not None
        return piece.piece_type == chess.PAWN and rank in (0, 7)

    def pick_up_piece_at(self, square: chess.Square) -> None:
        """
        If there is a piece on the square provided, pick it up. Otherwise, do
        nothing.
        """
        if self.board.piece_at(square) is not None:
            self.source_square = square

    def reset(self) -> None:
        """Reset the board to the starting position."""
        self.board.reset()

    def undo_last_move(self) -> None:
        """Undo the last move made on the board."""
        try:
            self.board.pop()
        except IndexError:
            # If we can't go back a move, that's fine. Just don't do anything.
            pass
