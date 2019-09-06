from __future__ import annotations
import pygame
import typing
if typing.TYPE_CHECKING:
    from car import Car


class Graphics:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Bayers Simulator")

    def draw(self, object):
        self.window.fill((0, 0, 0))
        pygame.draw.rect(self.window, object.color, object.get_rect())
        pygame.display.update()
