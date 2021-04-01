from typing import Tuple

import pygame
import pygame.freetype

from src.points import Points
from src.pathfinders import greedy
from src.pathfinders import simple_swap


FPS = 60
BACKGROUND_COLOR = (32, 32, 32)
TEXT_COLOR = (255, 255, 255)
POINT_COLOR = (255, 128, 0)
LINE_COLOR = (0, 128, 0)
SHORTEST_PATH_COLOR = (255, 128, 0)
POINT_RADIUS = 5
PATHFINDERS = {
    "greedy": greedy.Greedy,
    "simple_swap": simple_swap.SimpleSwap
}


def run(n: int, window_size: Tuple[int, int], min_distance: int) -> None:
    pygame.init()
    pygame.display.set_caption("traveling salesperson")
    window = pygame.display.set_mode(window_size)
    clock = pygame.time.Clock()

    points = Points(n, window_size, min_distance)
    pathfinder = PATHFINDERS["simple_swap"](points)  # TODO: Get name from command line argument.

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
                    pathfinder.reset()
                elif event.key == pygame.K_SPACE:
                    paused = not paused
                elif event.key == pygame.K_RETURN:
                    paused = True
                    pathfinder.update()

        if not paused:
            pathfinder.update()

        window.fill(BACKGROUND_COLOR)

        if pathfinder.current_path:
            pygame.draw.aalines(
                window,
                LINE_COLOR,
                True,
                pathfinder.current_path
            )
        if pathfinder.shortest_path:
            pygame.draw.aalines(
                window,
                SHORTEST_PATH_COLOR,
                True,
                pathfinder.shortest_path
            )
        for p in points.points:
            pygame.draw.circle(
                window,
                POINT_COLOR,
                p,
                POINT_RADIUS
            )

        font.render_to(
            window,
            text_margin,
            f"fps: {clock.get_fps():.0f}"
        )
        font.render_to(
            window,
            text_margin + line_spacing,
            f"iteration: {pathfinder.iteration:.0f}"
        )
        font.render_to(
            window,
            text_margin + line_spacing * 2,
            f"distance: {pathfinder.current_distance:.0f}"
        )
        font.render_to(
            window,
            text_margin + line_spacing * 3,
            f"shortest distance (iterations):"
        )
        for i, text in enumerate(pathfinder.records[-20:]):  # only show the last 20 records
            font.render_to(
                window,
                text_margin + line_spacing * (i + 4),
                text
            )

        pygame.display.flip()
