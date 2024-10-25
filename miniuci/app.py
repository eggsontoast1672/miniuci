import asyncio

import chess
import chess.engine
import pygame
from chess.engine import UciProtocol, INFO_SCORE

from miniuci import graphics
from miniuci.config import Config
from miniuci.settings import WINDOW_WIDTH, WINDOW_HEIGHT


class App:
    def __init__(self, config: Config, engine: UciProtocol) -> None:
        self.board = chess.Board()
        self.clock = pygame.time.Clock()
        self.engine = engine
        self.graphics = graphics.Board()
        self.limit = config.limit
        self.running = True
        self.surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    def drop_piece_at(self, square: chess.Square) -> None:
        from_square = self.graphics.get_from_square()
        assert from_square is not None
        move = chess.Move(from_square, square)
        if self.is_promotion_move(move):
            move.promotion = chess.QUEEN
        if self.board.is_legal(move):
            self.board.push(move)
            self.graphics.clear_best_move()
        self.graphics.clear_from_square()

    async def handle_event(self, event: pygame.event.Event) -> None:
        match event.type:
            case pygame.KEYDOWN:
                await self.handle_keydown(event)
            case pygame.MOUSEBUTTONDOWN:
                square = self.graphics.get_square_under_mouse()
                if self.graphics.is_holding_piece():
                    self.drop_piece_at(square)
                else:
                    self.pick_up_piece_at(square)
            case pygame.MOUSEBUTTONUP:
                if not self.graphics.is_holding_piece():
                    return
                square = self.graphics.get_square_under_mouse()
                if square != self.graphics.get_from_square():
                    self.drop_piece_at(square)
            case pygame.QUIT:
                self.running = False

    async def handle_keydown(self, event: pygame.event.Event) -> None:
        match event.key:
            case pygame.K_f:
                self.graphics.flip_orientation()
            case pygame.K_r:
                self.board.reset()
                self.graphics.clear_best_move()
            case pygame.K_LEFT:
                self.undo_last_move()
            case pygame.K_SPACE:
                # We use create_task here because we don't need any return value
                # and this function is the one that makes all of the engine
                # calls.
                asyncio.create_task(self.display_best_move())

    def is_promotion_move(self, move: chess.Move) -> bool:
        piece = self.board.piece_at(move.from_square)
        if piece is None:
            return False
        rank = chess.square_rank(move.to_square)
        return piece.piece_type == chess.PAWN and rank in (0, 7)

    def pick_up_piece_at(self, square: chess.Square) -> None:
        if self.board.piece_at(square) is not None:
            self.graphics.set_from_square(square)

    async def run(self):
        while self.running:
            for event in pygame.event.get():
                await self.handle_event(event)
            self.graphics.draw(self.board, self.surface)
            pygame.display.flip()
            await asyncio.sleep(0.016)
        await self.engine.quit()
        pygame.quit()

    async def display_best_move(self) -> None:
        print("thinking...")
        result = await self.engine.play(self.board, self.limit, info=INFO_SCORE)
        score = result.info.get("score")
        if score is not None:
            self.graphics.set_score(score)
            print(f"[DEBUG] {score=}")

        # result.move.__bool__ will be false if either the move is None (how
        # stockfish signals a checkmate position), or the move is a null move (
        # how some other engines signal it)
        if not result.move:
            print("checkmate")
            return
        self.graphics.set_best_move(result.move)

    def undo_last_move(self) -> None:
        try:
            self.board.pop()
        except IndexError:
            pass
