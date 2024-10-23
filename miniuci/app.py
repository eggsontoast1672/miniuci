import argparse
import chess
import chess.engine
import pprint
import pygame

from miniuci import graphics
from miniuci.settings import WINDOW_WIDTH, WINDOW_HEIGHT


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    go_settings = parser.add_mutually_exclusive_group(required=True)
    go_settings.add_argument("--depth", type=int)
    go_settings.add_argument("--time", type=int)

    parser.add_argument("--engine", default="stockfish")
    parser.add_argument("--fen", default=chess.STARTING_FEN)

    return parser.parse_args()


class App:
    def __init__(self, config: argparse.Namespace) -> None:
        if config.depth:
            limit = chess.engine.Limit(depth=config.depth)
        else:
            limit = chess.engine.Limit(time=config.time / 1000)

        # Is there a better place for this call? Probably.
        pygame.init()

        self.board = chess.Board(config.fen)
        self.clock = pygame.time.Clock()
        self.engine = chess.engine.SimpleEngine.popen_uci(config.engine)
        self.graphics = graphics.Board()
        self.limit = limit
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

    def handle_event(self, event: pygame.event.Event) -> None:
        match event.type:
            case pygame.KEYDOWN:
                self.handle_keydown(event)
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

    def handle_keydown(self, event: pygame.event.Event) -> None:
        match event.key:
            case pygame.K_f:
                self.graphics.flip_orientation()
            case pygame.K_r:
                self.board.reset()
            case pygame.K_LEFT:
                self.undo_last_move()
            case pygame.K_SPACE:
                self.display_best_move()

    def is_promotion_move(self, move: chess.Move) -> bool:
        piece = self.board.piece_at(move.from_square)
        if piece is None:
            return False
        rank = chess.square_rank(move.to_square)
        return piece.piece_type == chess.PAWN and rank in (0, 7)

    def pick_up_piece_at(self, square: chess.Square) -> None:
        if self.board.piece_at(square) is not None:
            self.graphics.set_from_square(square)

    def run(self):
        while self.running:
            for event in pygame.event.get():
                self.handle_event(event)
            self.graphics.draw(self.board, self.surface)
            pygame.display.flip()
            self.clock.tick(60)
        self.engine.quit()
        pygame.quit()

    def display_best_move(self) -> None:
        line = None
        with self.engine.analysis(self.board) as analysis:
            for info in analysis:
                pprint.pprint(info)

                score = info.get("score")
                if score is not None:
                    self.graphics.set_score(score)

                if self.limit.time is not None:
                    if info.get("time", 0) >= self.limit.time:
                        line = info.get("pv")
                        break
                elif self.limit.depth is not None:
                    if info.get("seldepth", 0) >= self.limit.depth:
                        line = info.get("pv")
                        break
                else:
                    # We can only limit the engine by time or depth at this
                    # point.
                    assert False, "unreachable"
        assert line is not None
        self.graphics.set_best_move(line[0])

    def undo_last_move(self) -> None:
        try:
            self.board.pop()
        except IndexError:
            pass
