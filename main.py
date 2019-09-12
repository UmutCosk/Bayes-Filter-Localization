# from __future__ import annotations  # type annotations
# import typing
from graphic import Graphic
from graphic import Color
import random
import pygame
import time
import numpy as np
pygame.init()


class Grid:
    def __init__(self, columns, rows, size, padding):
        self.cells = []
        self.rows = rows
        self.columns = columns
        self.size = size
        self.padding = padding
        self.green_count = 0
        self.red_count = 0
        color_random = [Color.Red.value, Color.Green.value]
        index = 0
        for i in range(rows):
            new = []
            for j in range(columns):
                color = color_random[random.randint(0, 1)]
                if(color == Color.Red.value):
                    self.red_count += 1
                else:
                    self.green_count += 1
                new.append(Cell(self.get_grid_x(j+1),
                                self.get_grid_y(i+1), self.size, 1/(rows*columns),  color, index, j, i))
                index += 1
            self.cells.append(new)

        self.cells = np.swapaxes(self.cells, 0, 1)

    def draw_cells(self, screen):
        for row in range(self.rows):
            for column in range(self.columns):
                alpha = 200 * self.cells[column][row].probability + 25
                alpha = alpha**(1.2)
                if(alpha > 255):
                    alpha = 255
                screen.draw_area(
                    self.cells[column][row].color, self.cells[column][row].rect, alpha)

    def get_grid_x(self, x):
        return self.padding*x+(x-1)*self.size

    def get_grid_y(self, y):
        return self.padding*y+(y-1)*self.size

    # def get_cell_index(self, x, y):
    #     index = 0
    #     counter = 0
    #     for i in range(self.rows):
    #         for j in range(self.columns):
    #             if(self.cells[counter].x_grid == x and self.cells[counter].y_grid == y):
    #                 index = counter
    #             counter += 1
    #     return index

    def measure_color(self, x, y, measure_uncertainty):
        true_color = self.cells[x-1][y-1].color
        color = true_color
        if(random.random() <= measure_uncertainty):
            if(true_color == Color.Red.value):
                color = Color.Green.value
            else:
                color = Color.Red.value
        return color

    def algorithm(self, measurement):
        new_probs = np.zeros((columns, rows))
        for column in range(rows):
            for row in range(columns):
                if(self.cells[column][row].color == measurement):
                    new_probs[column][row] = self.cells[column][row].probability * 10000
                else:
                    new_probs[column][row] = self.cells[column][row].probability * 0.1
        new_probs = np.dot(new_probs, 1/np.sum(new_probs))
        for row in range(rows):
            for column in range(columns):
                self.cells[column][row].probability = new_probs[column][row]

        # # a-prio
        # for row in range(rows):
        #     for column in range(columns):
        #         if(self.cells[column][row].color == measurement):
        #             new_probs[column][row] = self.cells[column][row].probability * 100
        #         else:
        #             new_probs[column][row] = self.cells[column][row].probability * 0.1
        # print(new_probs)
        # new_probs = np.dot(new_probs, 1/np.sum(new_probs))
        # print(new_probs)
        # for row in range(rows):
        #     for column in range(columns):
        #         self.cells[column][row].probability = new_probs[column][row]


class Cell:
    def __init__(self, x, y, size, probability, color, index, x_grid, y_grid):
        self.x = x
        self.y = y
        self.rect = (x, y, size, size)
        self.probability = probability
        self.color = color
        self.index = index
        self.x_grid = x_grid
        self.y_grid = y_grid


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

    def blur(self, blur_around_x, blur_around_y, blur_radius, grid):
        print(blur_around_x)
        print(blur_around_y)
        grid.cells[blur_around_x][blur_around_y].probability = grid.cells[blur_around_x][blur_around_y].probability*1.2
        for dx in range(blur_around_x-blur_radius, blur_around_x+blur_radius+1):
            for dy in range(blur_around_y-blur_radius, blur_around_y+blur_radius+1):
                if(not(dx < 0 or dy < 0) and not (dx == blur_around_x and dy == blur_around_y)and not(dx > columns-1 or dy > rows-1)):
                    grid.cells[dx][dy].probability = grid.cells[dx][dy].probability * 1.1
        # norm
        summe = 0
        for row in range(rows):
            for column in range(columns):
                summe += grid.cells[column][row].probability
        norm = 1/summe
        for row in range(rows):
            for column in range(columns):
                grid.cells[column][row].probability *= norm

    def move_player(self, grid):
        moved = False
        keys = pygame.key.get_pressed()
        if(keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_UP] or keys[pygame.K_DOWN]):
            moved = True
            if keys[pygame.K_LEFT]:
                self.grid_x -= 1
                if(self.grid_x < 1):
                    moved = False
                    self.grid_x = 1
            if keys[pygame.K_RIGHT]:
                self.grid_x += 1
                if(self.grid_x > columns):
                    moved = False
                    self.grid_x = columns
            if keys[pygame.K_UP]:
                self.grid_y -= 1
                if(self.grid_y < 1):
                    moved = False
                    self.grid_y = 1
            if keys[pygame.K_DOWN]:
                self.grid_y += 1
                if(self.grid_y > rows):
                    moved = False
                    self.grid_y = rows
        self.update_rect()
        if(moved):
            self.blur(blur_around_x=(self.grid_x-1),
                      blur_around_y=(self.grid_y-1), blur_radius=1, grid=grid)
        return moved

    def update_rect(self):
        self.x = grid.get_grid_x(self.grid_x)+round((grid.size-self.size)/2)
        self.y = grid.get_grid_y(self.grid_y)+round((grid.size-self.size)/2)
        self.rect = (self.x, self.y, self.size, self.size)


class BayesFilter:
    def __init__(self, grid):
        self.measure_certainty = 0.90
        self.green_probs = []
        self.red_probs = []

    # def algorithm(self, measurement):
    #     new_probs = []
    #     for row in range(rows):
    #         new = []
    #         for column in range(columns):
    #             new.append(0)
    #         new_probs.append(new)
    #     new_probs = np.swapaxes(new_probs, 0, 1)
    #     # a-prio
    #     for row in range(rows):
    #         for column in range(columns):
    #             if(grid.cells[column][row].color == measurement):
    #                 new_probs[column][row] = grid.cells[column][row].probability
    #             else:
    #                 new_probs[column][row] = grid.cells[column][row].probability
    #     print(new_probs)
    #     new_probs = np.dot(new_probs, 1/np.sum(new_probs))


pygame.font.init()
font = pygame.font.SysFont(None, 25)
text_offset = 10


def real_position_display(screen, player):
    real_position_text = font.render(
        "Real position: x: "+str(player.grid_x)+", y: "+str(player.grid_y), True, Color.Blue.value)
    screen.blit_text(real_position_text, (screen.width-screen.text_width+text_offset,
                                          text_offset, 100, 100))


def estimated_position_display(screen, x_ext, y_est):
    estimated_position_text = font.render(
        "Estimated position: x: "+str(x_ext)+", y: "+str(y_est), True, Color.Green.value)
    screen.blit_text(estimated_position_text, (screen.width-screen.text_width+text_offset,
                                               text_offset+100, 100, 100))


columns = 5  # X
rows = 5  # Y
measure_uncertainty = 0.10

screen = Graphic(800, 800, "Bayes Filter")
grid = Grid(columns, rows, 37, 5)

init_x = random.randint(1, columns)
init_y = random.randint(1, rows)
player = Player(grid, init_x, init_y, 15, Color.Blue.value)
bayes_filter = BayesFilter(grid)


run = True
while run:

    # Set Background
    screen.get_background()
    # Draw Cells
    grid.draw_cells(screen)
    # Draw Player
    player.draw_player(screen)
    time.sleep(0.1)
    # Player moves
    moved = player.move_player(grid)

    if(moved):
        color = grid.measure_color(
            player.grid_x, player.grid_y, measure_uncertainty)
        grid.algorithm(color)

    real_position_display(screen, player)
    # Refresh
    screen.update_screen()
    # Exit Condition
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


pygame.quit()
