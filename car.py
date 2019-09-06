import pygame


class Car:
    def __init__(self, x_start, y_start, width, height, color, velocity_start):
        self.x = x_start
        self.y = y_start
        self.width = width
        self.height = height
        self.color = color
        self.velocity = velocity_start

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x -= self.velocity
        if keys[pygame.K_RIGHT]:
            self.x += self.velocity
        if keys[pygame.K_UP]:
            self.y -= self.velocity
        if keys[pygame.K_DOWN]:
            self.y += self.velocity

    def get_rect(self):
        rect = (self.x, self.y, self.width, self.height)
        return rect
