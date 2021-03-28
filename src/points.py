from typing import List, Tuple
import random

import pygame


MARGIN_LEFT = 80  # space for the text
MARGIN_TOP = 100  # space for the text
MARGIN_RIGHT = 20
MARGIN_BOTTOM = 20


class Points:
    def __init__(self, n: int, window_size: Tuple[int, int], min_distance: int):
        self.n = n
        self.window_width, self.window_height = window_size
        self.min_distance = min_distance
        self.points = self.generate_points()
        self.distances = self.calculate_distances()

    def generate_points(self) -> Tuple[pygame.Vector2, ...]:
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
        return tuple(new_points)

    def calculate_distances(self) -> Tuple[Tuple[float, ...], ...]:
        # I could half the required space by only using a traingle of the distance matrix.
        # But then each time I want to query a distance I would need to check which
        # index is bigger than the other to get the correct row and column.
        # Then I could also remove the zero-diagonal.
        distances = [[0.0] * self.n for _ in range(self.n)]
        for i, p1 in enumerate(self.points[:-1]):
            for j, p2 in enumerate(self.points[i+1:], i + 1):
                distances[i][j] = distances[j][i] = p1.distance_to(p2)
        return tuple(tuple(x) for x in distances)

    def make_new_points(self) -> None:
        self.points = self.generate_points()
        self.distances = self.calculate_distances()

    # def get_distance(self, path: Sequence[pygame.Vector2]) -> float:
    #     distance = 0.0
    #     for i, p1 in enumerate(path):
    #         p2 = path[(i + 1) % self.n]
    #         distance += p1.distance_to(p2)
    #     return distance
    # TODO: the path argument should be a sequence of indices instead of points
