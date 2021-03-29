# Greedy search. Connect to the next closest point.

from typing import TYPE_CHECKING
import random
from math import inf

from src.pathfinders.pathfinder import Pathfinder

if TYPE_CHECKING:
    from src.points import Points


class Greedy(Pathfinder):
    def __init__(self, points_container: "Points"):
        super().__init__(points_container)

    def update(self) -> None:
        # Choose random start index. Then go to the next closest point.
        i = random.randint(0, self.points_container.n - 1)
        self.current_path = [self.points_container.points[i]]
        seen = {i}
        current_distance = 0.0
        while len(self.current_path) < self.points_container.n:
            distances = self.points_container.distances[i]
            min_distance = inf
            for j, d in enumerate(distances):
                if min_distance > d > 0 and j not in seen:
                    min_distance = d
                    i = j
            self.current_path.append(self.points_container.points[i])
            current_distance += min_distance
            seen.add(i)

        if current_distance < self.shortest_distance:
            self.shortest_distance = current_distance
            self.shortest_path = self.current_path
