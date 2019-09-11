import pygame
from enum import Enum
from rect import Rect
from rect import CollisionSpot
from bayes import BayesFilter
import time


class Car:
    def __init__(self, x_start, y_start, width, height, color, velocity, detection_radius):
        self.x = x_start
        self.y = y_start
        self.width = width
        self.height = height
        self.color = color
        self.velocity = velocity
        self.moving = False
        self.rect = Rect(self.width, self.height, self.x, self.y)
        self.currentCollision = CollisionSpot.NONE
        self.detect_radius = detection_radius

    def move(self, screen_width, screen_height, map_layout, bayes_filter, update):
        keys = pygame.key.get_pressed()
        if(keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_UP] or keys[pygame.K_DOWN]):
            self.moving = True
            if keys[pygame.K_LEFT]:
                if(self.currentCollision != CollisionSpot.LEFT):
                    self.x -= self.velocity
                    self.rect = self.rect.update_rect(self.x, self.y)
            if keys[pygame.K_RIGHT]:
                if(self.currentCollision != CollisionSpot.RIGHT):
                    self.x += self.velocity
                    self.rect = self.rect.update_rect(self.x, self.y)
            if keys[pygame.K_UP]:
                if(self.currentCollision != CollisionSpot.TOP):
                    self.y -= self.velocity
                    self.rect = self.rect.update_rect(self.x, self.y)
            if keys[pygame.K_DOWN]:
                if(self.currentCollision != CollisionSpot.BOTTOM):
                    self.y += self.velocity
                    self.rect = self.rect.update_rect(self.x, self.y)
        else:
            self.moving = False
        if(self.moving and update):
            bayes_filter.set_priori_position(self.x, self.y)
            #bayes_filter.flaten_around(self.x, self.y)
            print(bayes_filter.get_best_probability())
            update = False
        return update
