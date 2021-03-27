from typing import Sequence, Tuple
import random

import pygame


BEST_LEN_MAX = 10
MIN_DISTANCE = 20  # Min distance between points. TODO: implement this.
MARGIN_LEFT = 80  # space for the text
MARGIN_TOP = 100  # space for the text
MARGIN_RIGHT = 10
MARGIN_BOTTOM = 10


class Points:
    def __init__(self, n: int, window_size: Tuple[int, int]):
        self.n = n
        self.window_width, self.window_height = window_size
        self.points: Tuple[pygame.Vector2, ...] = ()
        self.generate_points()

        # TODO: Distance matrix for improved speed? Pre-calculate all distances
        #  so it is not necessary to do every update.

        # TODO: Method to return the distances from one point to all other points?
        # TODO: Maybe the algorithm just needs the indices and Points handles the coordinates?

        # self.n_lines = n
        # self.current_path: List[pygame.Vector2] = []
        # self.current_distance = inf
        # self.shortest_path = self.current_path
        # self.shortest_distance = self.current_distance

        # self.i = 0
        # self.best = [f"{self.shortest_distance:.0f} ({self.i})"]  # TODO: use fixed size deque?

    def generate_points(self) -> None:
        new_points = []
        for _ in range(self.n):
            p = pygame.Vector2(
                random.randrange(MARGIN_TOP, self.window_width - MARGIN_RIGHT),
                random.randrange(MARGIN_LEFT, self.window_height - MARGIN_BOTTOM)
            )
            new_points.append(p)
        self.points = tuple(new_points)

    def get_distance(self, path: Sequence[pygame.Vector2]) -> float:
        distance = 0.0
        for i, p1 in enumerate(path):
            p2 = path[(i + 1) % self.n]
            distance += p1.distance_to(p2)
        return distance
