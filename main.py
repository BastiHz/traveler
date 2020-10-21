import argparse
import random
from typing import List, Optional

import pygame
import pygame.freetype


WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
FPS = 60

BACKGROUND_COLRO = (32, 32, 32)
POINT_LINE_COLOR = (0, 255, 0)
POINT_RADIUS = 5
MIN_DISTANCE = 50


class PointList:
    def __init__(self, n: int, closed: bool) -> None:
        self.n = n
        self.closed = closed
        # Pre-compute valid positions so points are not too close to each other.
        self.valid_positions = []
        for x in range(MIN_DISTANCE, WINDOW_WIDTH, MIN_DISTANCE):
            for y in range(MIN_DISTANCE, WINDOW_HEIGHT, MIN_DISTANCE):
                self.valid_positions.append(pygame.Vector2(x, y))
        self.points: List[pygame.Vector2] = []
        self.distance = 0.0
        self.n_lines = n
        if not self.closed:
            self.n_lines -= 1

        self.new_points()
        self.update_distance()

    def new_points(self) -> None:
        self.points = random.sample(self.valid_positions, self.n)
        self.update_distance()

    def update_distance(self) -> None:
        self.distance = 0.0
        for i in range(self.n_lines):
            a = self.points[i]
            b = self.points[(i + 1) % self.n]
            self.distance += a.distance_to(b)

    def swap(self) -> None:
        i, j = random.sample(range(self.n), 2)
        self.points[i], self.points[j] = self.points[j], self.points[i]
        self.update_distance()

    def draw(self, target_surface: pygame.surface.Surface) -> None:
        pygame.draw.aalines(
            target_surface,
            POINT_LINE_COLOR,
            self.closed,
            self.points
        )
        for p in self.points:
            pygame.draw.circle(
                target_surface,
                POINT_LINE_COLOR,
                p,
                POINT_RADIUS
            )


def run(n: int, path_open: bool) -> None:
    pygame.init()
    pygame.display.set_caption("traveling salesperson")
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()

    points = PointList(n, not path_open)

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
                    points.new_points()

        points.swap()

        window.fill(BACKGROUND_COLRO)
        points.draw(window)
        font.render_to(window, (5, 5), f"total distance: {points.distance:.0f}")
        pygame.display.flip()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("n", type=int, help="Number of points.")
    parser.add_argument("-o", "--open", action="store_true",
                        help="Don't let the path return to the beginning.")
    args = parser.parse_args()
    run(args.n, args.open)
