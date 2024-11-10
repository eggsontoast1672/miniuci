from chess import Board
import pygame

from second_refactor import draw


def main() -> None:
    pygame.init()

    screen = pygame.display.set_mode((640, 640))
    clock = pygame.time.Clock()
    board = Board()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        draw.board(screen)
        draw.pieces(screen, board, None)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
