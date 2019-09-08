import pygame
from enum import Enum
from rect import Rect
from rect import CollisionSpot


class Car:
    def __init__(self, x_start, y_start, width, height, color, velocity):
        self.x = x_start
        self.y = y_start
        self.width = width
        self.height = height
        self.color = color
        self.velocity = velocity
        self.moving = False
        self.rect = Rect(self.width, self.height, self.x, self.y)

    def move(self, screen_width, screen_height, map_layout):
        keys = pygame.key.get_pressed()
        if(keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_UP] or keys[pygame.K_DOWN]):
            self.moving = True
            if keys[pygame.K_LEFT]:
                if(not self.rect.colliding_wall(CollisionSpot.LEFT, map_layout)):
                    self.x -= self.velocity
                    self.rect = self.rect.update_rect(self.x, self.y)
            if keys[pygame.K_RIGHT]:
                if(not self.rect.colliding_wall(CollisionSpot.RIGHT, map_layout)):
                    self.x += self.velocity
                    self.rect = self.rect.update_rect(self.x, self.y)
            if keys[pygame.K_UP]:
                if(not self.rect.colliding_wall(CollisionSpot.TOP, map_layout)):
                    self.y -= self.velocity
                    self.rect = self.rect.update_rect(self.x, self.y)
            if keys[pygame.K_DOWN]:
                if(not self.rect.colliding_wall(CollisionSpot.BOTTOM, map_layout)):
                    self.y += self.velocity
                    self.rect = self.rect.update_rect(self.x, self.y)

        else:
            self.moving = False
