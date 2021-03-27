# Greedy search. Connect to the next closest point.

# def greedy(self) -> List[pygame.Vector2]:
#     points = self.shortest_path.copy()
#     random.shuffle(points)
#     greedy_path = [points.pop()]
#     while points:
#         distances = [greedy_path[-1].distance_squared_to(p) for p in points]
#         min_dist_idx = distances.index(min(distances))
#         greedy_path.append(points.pop(min_dist_idx))
#     return greedy_path


# class Greedy:
#     def __init__(self, points):
#         self.points = points
#
#     def update(self):
#         pass
