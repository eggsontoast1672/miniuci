import argparse
from typing import Self

import chess
import pygame

import graphics
from engine import Engine
from settings import WINDOW_SIZE


class Config:
    def __init__(
        self, engine_path: str, search_time_millis: int, starting_fen: str
    ) -> None:
        self.engine_path = engine_path
        self.search_time_millis = search_time_millis
        self.starting_fen = starting_fen

    @classmethod
    def from_namespace(cls, namespace: argparse.Namespace) -> Self:
        return cls(namespace.engine, namespace.time, namespace.fen)

    @classmethod
    def parse(cls) -> Self:
        parser = argparse.ArgumentParser()
        parser.add_argument("--engine", default="/usr/games/stockfish")
        parser.add_argument("--fen", default=chess.STARTING_FEN)
        parser.add_argument("--time", default=4000)

        return cls.from_namespace(parser.parse_args())


def can_promote(move: chess.Move, board: chess.Board) -> bool:
    piece = board.piece_at(move.from_square)
    if piece is None or piece.piece_type != chess.PAWN:
        return False

    if piece.color == chess.BLACK:
        return chess.square_rank(move.to_square) == 0
    else:
        return chess.square_rank(move.to_square) == 7


def main() -> None:
    pygame.init()

    config = Config.parse()
    board = graphics.Board(
        board=chess.Board(config.starting_fen),
        engine=Engine(config.engine_path, config.search_time_millis),
        surface=pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE)),
    )

    clock = pygame.time.Clock()

    window_should_close = False

    while not window_should_close:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    board.flip_orientation()
                elif event.key == pygame.K_SPACE:
                    board.display_best_move()
                elif event.key == pygame.K_r:
                    board.reset()
                elif event.key == pygame.K_LEFT:
                    board.undo_last_move()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                square = board.get_square(pygame.mouse.get_pos())
                if board.is_holding_piece():
                    board.drop_piece_at(square)
                else:
                    board.pick_up_piece_at(square)
            elif event.type == pygame.MOUSEBUTTONUP:
                if not board.is_holding_piece():
                    continue
                square = board.get_square(pygame.mouse.get_pos())
                if square != board.source_square:
                    board.drop_piece_at(square)
            elif event.type == pygame.QUIT:
                window_should_close = True

        board.draw()
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
