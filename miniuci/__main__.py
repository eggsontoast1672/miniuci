import argparse
from typing import Self

import chess
import pygame

import graphics
from engine import Engine, Search, SearchKind
from settings import WINDOW_SIZE


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    go_settings = parser.add_mutually_exclusive_group()
    go_settings.add_argument("--depth", type=int)
    go_settings.add_argument("--time", type=int)

    parser.add_argument("--engine", default="stockfish")
    parser.add_argument("--fen", default=chess.STARTING_FEN)

    return parser.parse_args()


def main() -> None:
    pygame.init()

    config = parse_args()
    if config.depth:
        search = Search(SearchKind.DEPTH, config.depth)
    elif config.time:
        search = Search(SearchKind.TIME, config.time)
    else:
        print("need depth or time")
        return

    board = graphics.Board(
        board=chess.Board(config.fen),
        engine=Engine(config.engine, search),
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
