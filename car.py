from __future__ import annotations
import pygame
import typing
if typing.TYPE_CHECKING:
    from graphics import Graphics


class Car:
    def __init__(self, x_start, y_start, width, height, color, velocity):
        self.x = x_start
        self.y = y_start
        self.width = width
        self.height = height
        self.color = color
        self.velocity = velocity

    def move(self, window: Graphics):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.x > self.width/2:
            self.x -= self.velocity
        if keys[pygame.K_RIGHT] and self.x < window.width - (self.width*1.5):
            self.x += self.velocity
        if keys[pygame.K_UP] and self.y > self.height/2:
            self.y -= self.velocity
        if keys[pygame.K_DOWN] and self.y < window.height - (self.height*1.2):
            self.y += self.velocity

    def get_rect(self):
        rect = (self.x, self.y, self.width, self.height)
        return rect
