import pygame
from enum import Enum


class CollisionSpot(Enum):
    LEFT = 0
    RIGHT = 1
    TOP = 2
    BOTTOM = 3


class Car:
    def __init__(self, x_start, y_start, width, height, color, velocity):
        self.x = x_start
        self.y = y_start
        self.width = width
        self.height = height
        self.color = color
        self.velocity = velocity
        self.moving = False

    def move(self, window_width, window_height, map_layout):
        keys = pygame.key.get_pressed()
        if(keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_UP] or keys[pygame.K_DOWN]):
            self.moving = True
            if keys[pygame.K_LEFT] and self.x > round(self.width/2):
                if(not self.is_colliding(CollisionSpot.LEFT, map_layout)):
                    self.x -= self.velocity
            if keys[pygame.K_RIGHT] and self.x < window_width - round((self.width*1.5)):
                if(not self.is_colliding(CollisionSpot.RIGHT, map_layout)):
                    self.x += self.velocity
            if keys[pygame.K_UP] and self.y > round(self.height/2):
                if(not self.is_colliding(CollisionSpot.TOP, map_layout)):
                    self.y -= self.velocity
            if keys[pygame.K_DOWN] and self.y < window_height - round((self.height*1.2)):
                if(not self.is_colliding(CollisionSpot.BOTTOM, map_layout)):
                    self.y += self.velocity
        else:
            self.moving = False

    def get_rect(self):
        rect = (self.x, self.y, self.width, self.height)
        return rect

    def is_colliding(self, collision_spot, map_layout):
        coliding = False
        collision_offset = 2
        if(collision_spot == CollisionSpot.LEFT):
            if(map_layout[self.y+round(self.height/2), self.x-collision_offset] == 0):
                coliding = True
        if(collision_spot == CollisionSpot.RIGHT):
            if(map_layout[self.y+round(self.height/2), self.x+self.width+collision_offset] == 0):
                coliding = True
        if(collision_spot == CollisionSpot.TOP):
            if(map_layout[self.y-collision_offset, self.x+round(self.width/2)] == 0):
                coliding = True
        if(collision_spot == CollisionSpot.BOTTOM):
            if(map_layout[self.y+self.height+collision_offset, self.x+round(self.width/2)] == 0):
                coliding = True
        return coliding
