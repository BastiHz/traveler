# Randomly swap two connections.

from typing import TYPE_CHECKING
import random

from src.pathfinders.pathfinder import Pathfinder
from src.pathfinders.greedy import Greedy

if TYPE_CHECKING:
    from src.points import Points


class SimpleSwap(Pathfinder):
    def __init__(self, points_container: "Points") -> None:
        super().__init__(points_container)

        # Start by creating a greedy path.
        self.g = Greedy(points_container)

    def update(self) -> None:
        if self.iteration == 0:
            self.g.update()
            self.current_path = self.g.current_path
            self.shortest_path = self.g.shortest_path
            self.shortest_distance = self.g.shortest_distance
            self.iteration = 1
            return
        self.iteration += 1
        i, j = random.sample(range(self.points_container.n), 2)
        self.current_path = self.shortest_path.copy()
        self.current_path[i], self.current_path[j] = self.current_path[j], self.current_path[i]
        new_distance = self.points_container.calculate_total_distance(self.current_path)
        # TODO: hier weiter




    def reset(self):
        self.g.reset()
        super().reset()
        self.current_path_indices = []
        self.shortest_path_indices = []
