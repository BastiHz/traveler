from typing import TYPE_CHECKING, List
from math import inf

if TYPE_CHECKING:
    from src.points import Points
    from pygame import Vector2


class Pathfinder:
    def __init__(self, points_container: "Points"):
        self.points_container = points_container
        self.current_path: List[Vector2] = []
        self.shortest_path: List[Vector2] = []
        self.current_distance = 0.0
        self.shortest_distance = inf
        self.iteration = 0
        self.records = []

    def update(self) -> None:
        raise NotImplementedError

    def reset(self) -> None:
        self.iteration = 0
        self.current_path = []
        self.shortest_path = []
        self.shortest_distance = inf
        self.current_distance = 0.0
        self.records = []
