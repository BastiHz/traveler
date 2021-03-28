from typing import Tuple

import pygame
import pygame.freetype

from src.points import Points
# from src.greedy import Greedy
# from src.simple_swap import simple_swap


FPS = 60
BACKGROUND_COLOR = (32, 32, 32)
TEXT_COLOR = (255, 255, 255)
POINT_COLOR = (255, 128, 0)
LINE_COLOR = (0, 128, 0)
SHORTEST_PATH_COLOR = (255, 128, 0)
POINT_RADIUS = 5


def run(n: int, window_size: Tuple[int, int], min_distance: int) -> None:
    pygame.init()
    pygame.display.set_caption("traveling salesperson")
    window = pygame.display.set_mode(window_size)
    clock = pygame.time.Clock()

    points = Points(n, window_size, min_distance)
    # algorithm = Greedy(points)

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
                    points.generate_points()
                elif event.key == pygame.K_SPACE:
                    paused = not paused
                elif event.key == pygame.K_RETURN:
                    paused = True
                    # algorithm.update()

        # if not paused:
        #     algorithm.update()

        window.fill(BACKGROUND_COLOR)

        for p in points.points:
            pygame.draw.circle(
                window,
                POINT_COLOR,
                p,
                POINT_RADIUS
            )

        # (draw paths)
        # draw shortest path

        font.render_to(
            window,
            text_margin,
            f"fps: {clock.get_fps():.0f}"
        )
        # font.render_to(
        #     window,
        #     text_margin + line_spacing,
        #     f"current distance: {points.current_distance:.0f}"
        # )
        # font.render_to(
        #     window,
        #     text_margin + line_spacing * 2,
        #     f"shortest distance (iterations):"
        # )
        # for i, best in enumerate(points.best):
        #     font.render_to(
        #         window,
        #         text_margin + line_spacing * (i + 3),
        #         best
        #     )

        pygame.display.flip()
