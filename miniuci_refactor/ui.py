import asyncio
import dataclasses
import math
from typing import ClassVar, Optional

import chess
import pygame
from chess import Board, Move, Square
from chess.engine import Limit, UciProtocol
from pygame import Rect, Surface, Vector2
from pygame.event import Event

from miniuci.resources import ResourceManager


@dataclasses.dataclass
class BoardProps:
    best_move: Optional[Move]
    board: Board
    orientation: chess.Color


class BoardComponent:
    RECT: ClassVar[Rect] = Rect(0, 0, 640, 640)
    CELL_SIZE: ClassVar[Vector2] = Vector2(RECT.width / 8, RECT.height / 8)

    COLOR_BEST_SQUARE: ClassVar[pygame.Color] = pygame.Color(0xFF, 0xFF, 0x00)
    COLOR_DARK_SQUARE: ClassVar[pygame.Color] = pygame.Color(0xB5, 0x88, 0x63)
    COLOR_FROM_SQUARE: ClassVar[pygame.Color] = pygame.Color(0xFF, 0x00, 0x00)
    COLOR_LIGHT_SQUARE: ClassVar[pygame.Color] = pygame.Color(0xF0, 0xD9, 0xB5)

    def __init__(self) -> None:
        self.from_square: Optional[Square] = None
        self.manager = ResourceManager()
        self.surface = Surface(self.RECT.size)

    def get_mouse_pos(self) -> Vector2:
        pos = pygame.mouse.get_pos()
        return Vector2(pos[0] + self.RECT.x, pos[1] + self.RECT.y)

    def get_square_color(self, square: Square, props: BoardProps) -> pygame.Color:
        pos = self.get_square_pos(square, props)
        if self.is_square_best_move(square, props):
            return self.COLOR_BEST_SQUARE
        elif square == self.from_square:
            return self.COLOR_FROM_SQUARE
        elif (pos.x + pos.y) % 2 == 0:
            return self.COLOR_LIGHT_SQUARE
        else:
            return self.COLOR_DARK_SQUARE

    def get_square_pos(self, square: Square, props: BoardProps) -> Vector2:
        file = chess.square_file(square)
        rank = chess.square_rank(square)
        if props.orientation:
            return Vector2(file, 7 - rank)
        else:
            return Vector2(7 - file, rank)

    def get_square_under_mouse(self, props: BoardProps) -> Square:
        pos = self.get_mouse_pos()
        file = math.floor(pos.x / self.CELL_SIZE.x)
        rank = math.floor(pos.y / self.CELL_SIZE.y)
        if props.orientation:
            return chess.square(file, 7 - rank)
        else:
            return chess.square(7 - file, rank)


    def is_square_best_move(self, square: Square, props: BoardProps) -> bool:
        if props.best_move is None:
            return False
        is_from_square = square == props.best_move.from_square
        is_to_square = square == props.best_move.to_square
        return is_from_square or is_to_square

    def on_key_down(self, event: Event) -> None:
        if event.key == pygame.K_r:
            self.from_square = None

    def on_mouse_down(self, props: BoardProps) -> None:
        # Get the square that was clicked
        # If we are not holding a piece:
        #     If there is a piece on the clicked square:
        #         Pick up the piece
        #     Otherwise:
        #         Do nothing
        # Otherwise:
        #     If the clicked square is empty:
        #         Place the held piece on that square
        #     Otherwise:
        #         Drop the piece back on its original square
        square = self.get_square_under_mouse(props)
        piece = props.board.piece_at(square)
        match self.from_square, piece:
            case None, None:
                return
            case None, _:
                self.from_square = square
            case _, _:
                move = Move(self.from_square, square)
                if props.board.is_legal(move):
                    props.board.push(move)
                self.from_square = None

    def render(self, props: BoardProps) -> Surface:
        self.render_background(props)
        self.render_pieces(props)
        return self.surface

    def render_background(self, props: BoardProps) -> None:
        for square in chess.SQUARES:
            pos = self.get_square_pos(square, props)
            color = self.get_square_color(square, props)
            rect = Rect(pos * self.CELL_SIZE.x, self.CELL_SIZE)
            pygame.draw.rect(self.surface, color, rect)

    def render_pieces(self, props: BoardProps) -> None:
        held_piece = None
        for color in chess.COLORS:
            for piece in chess.PIECE_TYPES:
                squares = props.board.pieces(piece, color)
                image = self.manager.get(piece, color)
                for square in squares:
                    if square == self.from_square:
                        held_piece = image
                        continue
                    elif props.orientation:
                        pos = Vector2(
                            chess.square_file(square), 7 - chess.square_rank(square)
                        )
                    else:
                        pos = Vector2(
                            7 - chess.square_file(square), chess.square_rank(square)
                        )
                    self.surface.blit(image, pos * self.CELL_SIZE.x)
        if held_piece is not None:
            mouse_pos = self.get_mouse_pos()
            self.surface.blit(held_piece, mouse_pos - self.CELL_SIZE / 2)


class RootComponent:
    # We need to inject the engine because we're using an async child process
    # and __init__ cannot be async.
    def __init__(self, engine: UciProtocol) -> None:
        self.best_move: Optional[Move] = None
        self.board = Board()
        self.engine = engine
        self.orientation = chess.WHITE
        self.surface = Surface((640, 640))

        # Components
        self.board_component = BoardComponent()

    async def display_best_move(self) -> None:
        with await self.engine.analysis(self.board, limit=Limit(depth=22)) as analysis:
            async for info in analysis:
                print(info)
                if (pv := info.get("pv")) is not None:
                    self.best_move = pv[0]
        print("done")

    def on_key_press(self, event: Event) -> None:
        match event.key:
            case pygame.K_f:
                self.orientation = not self.orientation
            case pygame.K_r:
                self.best_move = None
                self.board.reset()
                self.engine.send_line("stop")
            case pygame.K_LEFT:
                try:
                    self.board.pop()
                except IndexError:
                    pass
            case pygame.K_SPACE:
                asyncio.create_task(self.display_best_move())

        self.board_component.on_key_down(event)

    def on_mouse_down(self) -> None:
        self.board_component.on_mouse_down(BoardProps(self.best_move, self.board, self.orientation))

    def render(self) -> Surface:
        self.surface.blit(
            self.board_component.render(BoardProps(
                self.best_move,
                self.board,
                self.orientation)),
            self.board_component.RECT)
        return self.surface
