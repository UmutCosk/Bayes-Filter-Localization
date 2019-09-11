# from __future__ import annotations  # type annotations
# import typing
from graphic import Graphic
from graphic import Color
import random
import pygame
import time
pygame.init()


class Grid:
    def __init__(self, rows, columns, size, padding):
        self.cells = []
        self.size = size
        self.padding = padding
        color_random = [Color.Red.value, Color.Green.value]
        for i in range(rows+1):
            for j in range(columns+1):
                color = color_random[random.randint(0, 1)]
                self.cells.append(Cell(self.get_grid_x(i),
                                       self.get_grid_y(j), self.size, 1/(rows*columns),  color))

    def draw_cells(self, screen):
        for i in range(len(self.cells)):
            alpha = 200 * self.cells[i].probability + 55
            screen.draw_area(self.cells[i].color, self.cells[i].rect, alpha)

    def get_grid_x(self, x):
        return self.padding*x+self.size*(x-1)

    def get_grid_y(self, y):
        return self.padding*y+(y-1)*self.size


class Cell:
    def __init__(self, x, y, size, probability, color):
        self.x = x
        self.y = y
        self.rect = (x, y, size, size)
        self.probability = probability
        self.color = color


class Player:
    def __init__(self, grid, x, y, size, color):
        self.grid_x = x
        self.grid_y = y
        self.x = grid.get_grid_x(x)+round((grid.size-size)/2)
        self.y = grid.get_grid_y(y)+round((grid.size-size)/2)
        self.size = size
        self.rect = (self.x, self.y, size, size)
        self.color = color

    def draw_player(self, screen):
        screen.draw_area(self.color, self.rect, 255)

    def move_player(self, grid):
        keys = pygame.key.get_pressed()
        if(keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_UP] or keys[pygame.K_DOWN]):
            if keys[pygame.K_LEFT]:
                self.grid_x -= 1
                if(self.grid_x < 1):
                    self.grid_x = 1
            if keys[pygame.K_RIGHT]:
                self.grid_x += 1
                if(self.grid_x > 19):
                    self.grid_x = 19
            if keys[pygame.K_UP]:
                self.grid_y -= 1
                if(self.grid_y < 1):
                    self.grid_y = 1
            if keys[pygame.K_DOWN]:
                self.grid_y += 1
                if(self.grid_y > 19):
                    self.grid_y = 19
        self.update_rect()

    def update_rect(self):
        self.x = grid.get_grid_x(self.grid_x)+round((grid.size-self.size)/2)
        self.y = grid.get_grid_y(self.grid_y)+round((grid.size-self.size)/2)
        self.rect = (self.x, self.y, self.size, self.size)


screen = Graphic(800, 800, "Bayes Filter")
grid = Grid(19, 19, 37, 5)

init_x = random.randint(19, 19)
init_y = random.randint(19, 19)
player = Player(grid, init_x, init_y, 15, Color.Blue.value)

run = True
while run:
    # Set Background
    screen.get_background()
    # Draw Cells
    grid.draw_cells(screen)
    # Draw Player
    player.draw_player(screen)
    player.move_player(grid)

    # Refresh
    screen.update_screen()
    # Exit Condition
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


pygame.quit()
