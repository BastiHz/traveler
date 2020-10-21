import argparse
import random
from typing import List

import pygame
import pygame.freetype


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


def new_points(n: int) -> List:
    return random.sample(VALID_POSITIONS, n)


def get_distance(points: List[pygame.Vector2],
                 closed: bool) -> float:
    n_lines = len(points)
    if not closed:
        n_lines -= 1
    distance = 0.0
    for i in range(n_lines):
        a = points[i]
        b = points[(i + 1) % len(points)]
        distance += a.distance_to(b)
    return distance


def run(n: int, path_open: bool) -> None:
    pygame.init()
    pygame.display.set_caption("traveling salesperson")
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()

    points = new_points(n)
    closed = not path_open

    font = pygame.freetype.SysFont("inconsolate, consolas, monospace", 16)
    font.fgcolor = (255, 255, 255)

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
                    points = new_points(n)

        window.fill(BACKGROUND_COLRO)
        for p in points:
            pygame.draw.circle(window, POINT_COLOR, p, POINT_RADIUS)
        pygame.draw.aalines(window, POINT_COLOR, closed, points)

        distance = get_distance(points, closed)
        font.render_to(window, (5, 5), f"{distance=:.2f}")

        pygame.display.flip()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("n", type=int, help="Number of points.")
    parser.add_argument("-o", "--open", action="store_true",
                        help="Don't let the path return to the beginning.")
    args = parser.parse_args()
    run(args.n, args.open)
