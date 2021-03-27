import argparse
import random
from math import inf
from typing import List, Tuple

import pygame
import pygame.freetype


DEFAULT_WINDOW_SIZE = (800, 600)
FPS = 60

BACKGROUND_COLRO = (32, 32, 32)
POINT_COLOR = (255, 128, 0)
LINE_COLOR = (0, 128, 0)
SHORTEST_PATH_COLOR = (255, 128, 0)
TEXT_COLOR = (255, 255, 255)
POINT_RADIUS = 5
BEST_LEN_MAX = 10
MIN_DISTANCE = POINT_RADIUS * 4  # Min distance between points. TODO: implement this.
MARGIN_LEFT = 80  # space for the text
MARGIN_TOP = 100  # space for the text
MARGIN_RIGHT = 10
MARGIN_BOTTOM = 10


class PointList:
    def __init__(self, n: int, closed: bool, window_size: Tuple[int, int]) -> None:
        self.n = n
        self.closed = closed
        self.window_width, self.window_height = window_size
        self.n_lines = n
        if not self.closed:
            self.n_lines -= 1

        self.current_path: List[pygame.Vector2] = []
        self.current_distance = inf
        self.shortest_path = self.current_path
        self.shortest_distance = self.current_distance
        self.make_new_points()

        self.i = 0
        self.best = [f"{self.shortest_distance:.0f} ({self.i})"]  # TODO: use fixed size deque?

    def make_new_points(self) -> None:
        new_points = []
        for _ in range(self.n):
            p = pygame.Vector2(
                random.randrange(MARGIN_TOP, self.window_width - MARGIN_RIGHT),
                random.randrange(MARGIN_LEFT, self.window_height - MARGIN_BOTTOM)
            )
            new_points.append(p)
        self.shortest_path = new_points
        self.shortest_path = self.greedy()
        self.shortest_distance = self.get_distance(self.shortest_path)
        self.i = 0
        self.best = [f"{self.shortest_distance:.0f} ({self.i})"]
        self.current_path = self.shortest_path
        self.current_distance = self.shortest_distance

    def update(self) -> None:
        self.i += 1
        self.current_path = self.swap()
        self.current_distance = self.get_distance(self.current_path)
        if self.current_distance < self.shortest_distance:
            self.shortest_distance = self.current_distance
            self.shortest_path = self.current_path.copy()
            self.best.append(f"{self.shortest_distance:.0f} ({self.i})")
            if len(self.best) > BEST_LEN_MAX:
                self.best = self.best[1:]

    def get_distance(self, points: List[pygame.Vector2]) -> float:
        distance = 0.0
        for i in range(self.n_lines):
            a = points[i]
            b = points[(i + 1) % self.n]
            distance += a.distance_to(b)
        return distance

    def greedy(self) -> List[pygame.Vector2]:
        points = self.shortest_path.copy()
        random.shuffle(points)
        greedy_path = [points.pop()]
        while points:
            distances = [greedy_path[-1].distance_squared_to(p) for p in points]
            min_dist_idx = distances.index(min(distances))
            greedy_path.append(points.pop(min_dist_idx))
        return greedy_path

    def swap(self) -> List[pygame.Vector2]:
        points = self.shortest_path.copy()
        i, j = random.sample(range(self.n), 2)
        points[i], points[j] = points[j], points[i]
        return points

    def draw(self, target_surface: pygame.surface.Surface) -> None:
        pygame.draw.aalines(
            target_surface,
            LINE_COLOR,
            self.closed,
            self.current_path
        )
        pygame.draw.aalines(
            target_surface,
            SHORTEST_PATH_COLOR,
            self.closed,
            self.shortest_path,
            0
        )
        for p in self.current_path:
            pygame.draw.circle(
                target_surface,
                POINT_COLOR,
                p,
                POINT_RADIUS
            )


def run(n: int, path_open: bool, window_size: Tuple[int, int]) -> None:
    pygame.init()
    pygame.display.set_caption("traveling salesperson")
    window = pygame.display.set_mode(window_size)
    clock = pygame.time.Clock()

    points = PointList(n, not path_open, window_size)

    font = pygame.freetype.SysFont("inconsolate, consolas, monospace", 16)
    font.fgcolor = TEXT_COLOR
    line_spacing = pygame.Vector2(0, font.get_sized_height())
    text_margin = pygame.Vector2(5, 5)

    paused = True
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
                    paused = True
                    points.make_new_points()
                elif event.key == pygame.K_SPACE:
                    paused = not paused
                elif event.key == pygame.K_RETURN:
                    paused = True
                    points.update()

        if not paused:
            points.update()

        window.fill(BACKGROUND_COLRO)
        points.draw(window)
        font.render_to(
            window,
            text_margin,
            f"fps: {clock.get_fps():.0f}"
        )
        font.render_to(
            window,
            text_margin + line_spacing,
            f"current distance: {points.current_distance:.0f}"
        )
        font.render_to(
            window,
            text_margin + line_spacing * 2,
            f"shortest distance (iterations):"
        )
        for i, best in enumerate(points.best):
            font.render_to(
                window,
                text_margin + line_spacing * (i + 3),
                best
            )
        pygame.display.flip()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("n", type=int, help="Number of points.")
    parser.add_argument(
        "-o",
        "--open",
        action="store_true",
        help="Don't let the path return to the beginning."
    )
    parser.add_argument(
        "-w",
        "--window-size",
        metavar=("<width>", "<height>"),
        nargs=2,
        type=int,
        help="Specify the window width and height in pixels.",
        default=DEFAULT_WINDOW_SIZE
    )
    args = parser.parse_args()
    run(args.n, args.open, args.window_size)
