import asyncio
from typing import Optional

import chess
import chess.engine
import pygame
from chess import Board, Move, Square
from chess.engine import Cp, PovScore, UciProtocol

from miniuci.clock import AsyncClock
from miniuci.config import Config
from miniuci.settings import WINDOW_WIDTH, WINDOW_HEIGHT


class State:
    def __init__(self) -> None:
        self.best_move: Optional[Move] = None
        self.board = Board()
        self.engine_thinking = False
        self.from_square: Optional[Square] = None
        self.score = PovScore(Cp(0), chess.WHITE)
        self.white = True


class App:
    def __init__(self, config: Config, engine: UciProtocol) -> None:
        self.clock = AsyncClock()
        self.engine = engine
        self.limit = config.limit
        self.running = True
        self.surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.state = State()

    def drop_piece_at(self, square: chess.Square) -> None:
        assert self.state.from_square is not None
        move = chess.Move(self.state.from_square, square)
        if self.is_promotion_move(move):
            # TODO Promotion dialogue
            move.promotion = chess.QUEEN
        if self.state.board.is_legal(move):
            self.state.board.push(move)
            self.state.best_move = None

        # Reset board things
        self.interface.reset()

    async def handle_event(self, event: pygame.event.Event) -> None:
        match event.type:
            case pygame.KEYDOWN:
                await self.handle_keydown(event)
            case pygame.MOUSEBUTTONDOWN:
                square = self.interface.get_square_under_mouse()
                if self.interface.is_holding_piece():
                    self.drop_piece_at(square)
                else:
                    self.pick_up_piece_at(square)
            case pygame.MOUSEBUTTONUP:
                if not self.interface.is_holding_piece():
                    return
                square = self.interface.get_square_under_mouse()
                if square != self.interface.get_from_square():
                    self.drop_piece_at(square)
            case pygame.QUIT:
                self.running = False

    async def handle_keydown(self, event: pygame.event.Event) -> None:
        match event.key:
            case pygame.K_f:
                self.interface.flip_orientation()
            case pygame.K_r:
                self.board.reset()
                self.interface.reset()
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
            self.interface.set_from_square(square)

    async def run(self):
        while self.running:
            for event in pygame.event.get():
                await self.handle_event(event)
            # TODO: Fix me!!!
            self.interface.draw(self.board)
            self.surface.blit(self.interface.surface, (0, 0))
            pygame.display.flip()
            await self.clock.tick(60)
        await self.engine.quit()
        pygame.quit()

    async def display_best_move(self) -> None:
        self.interface.activate()
        with await self.engine.analysis(self.board, limit=self.limit) as analysis:
            async for info in analysis:
                print(info)

                # Eval bar
                score = info.get("score")
                if score is not None:
                    self.interface.set_score(score)

                # Best move
                pv = info.get("pv")
                if pv is not None:
                    self.interface.set_best_move(pv[0])
        self.interface.deactivate()

    def undo_last_move(self) -> None:
        try:
            self.board.pop()
        except IndexError:
            pass
