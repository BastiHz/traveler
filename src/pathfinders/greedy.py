# Greedy search. Connect to the next closest point.

import random


# def greedy(self) -> List[pygame.Vector2]:
#     points = self.shortest_path.copy()
#     random.shuffle(points)
#     greedy_path = [points.pop()]
#     while points:
#         distances = [greedy_path[-1].distance_squared_to(p) for p in points]
#         min_dist_idx = distances.index(min(distances))
#         greedy_path.append(points.pop(min_dist_idx))
#     return greedy_path


class Greedy:
    def __init__(self, points_container):
        self.points_container = points_container
        self.shortest_path = ()
        self.current_path = ()
        self.best_distance = 0.0

    def update(self):
        # Choose random start index. Then go to the next closest point.
        indices = list(range(self.points_container.n))
        i = random.choice(indices)
        indices.remove(i)
        while indices:
            # distances = sorted(self.points_container.distances[i])
            # I need the shortest distance > 0 and the index of it.


