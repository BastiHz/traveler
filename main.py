import argparse
import random

import pygame


WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
FPS = 60
BACKGROUND_COLRO = (32, 32, 32)
POINT_COLOR = (255, 128, 0)
POINT_RADIUS = 5
MIN_DISTANCE = 50
VALID_POSITIONS = []
for x in range(MIN_DISTANCE, WINDOW_WIDTH, MIN_DISTANCE):
    for y in range(MIN_DISTANCE, WINDOW_HEIGHT, MIN_DISTANCE):
        VALID_POSITIONS.append(pygame.Vector2(x, y))


def run(n: int, path_open: bool) -> None:
    pygame.init()
    pygame.display.set_caption("traveling salesperson")
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()
    points = random.sample(VALID_POSITIONS, n)

    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_n:
                    points = random.sample(VALID_POSITIONS, n)

        window.fill(BACKGROUND_COLRO)
        for p in points:
            pygame.draw.circle(window, POINT_COLOR, p, POINT_RADIUS)

        pygame.draw.aalines(window, POINT_COLOR, not path_open, points)
        pygame.display.flip()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("n", type=int, help="Number of points.")
    parser.add_argument("-o", "--open", action="store_true",
                        help="Don't let the path return to the beginning.")
    args = parser.parse_args()
    run(args.n, args.open)
