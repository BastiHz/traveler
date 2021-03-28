from typing import List, Sequence, Tuple
import random

import pygame


BEST_LEN_MAX = 10
MARGIN_LEFT = 80  # space for the text
MARGIN_TOP = 100  # space for the text
MARGIN_RIGHT = 20
MARGIN_BOTTOM = 20


class Points:
    def __init__(self, n: int, window_size: Tuple[int, int], min_distance: int):
        self.n = n
        self.window_width, self.window_height = window_size
        self.min_distance = min_distance
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
        new_points: List[pygame.Vector2] = []
        check_min_distance = True
        tries = 0
        # Make 1000 tries to place a point with enough space around it.
        # If that fails then place it and the rest of the points anywhere.
        while len(new_points) < self.n:
            new_point = pygame.Vector2(
                random.randrange(MARGIN_TOP, self.window_width - MARGIN_RIGHT),
                random.randrange(MARGIN_LEFT, self.window_height - MARGIN_BOTTOM)
            )
            if check_min_distance:
                tries += 1
                for p in new_points:
                    if p.distance_to(new_point) < self.min_distance:
                        break
                else:
                    # Point can be placed outside minimum distance.
                    new_points.append(new_point)
                    tries = 0
                if tries >= 1000:
                    # Not enough space, min distance not obeyed, place all other points anywhere.
                    print("Warning: Could not keep minimum distance between points.")
                    check_min_distance = False
            else:
                new_points.append(new_point)
        self.points = tuple(new_points)

    def get_distance(self, path: Sequence[pygame.Vector2]) -> float:
        distance = 0.0
        for i, p1 in enumerate(path):
            p2 = path[(i + 1) % self.n]
            distance += p1.distance_to(p2)
        return distance
