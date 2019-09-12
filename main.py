# from __future__ import annotations  # type annotations
# import typing
from graphic import Graphic
from graphic import Color
from enum import Enum
import random
import pygame
import time
import numpy as np
pygame.init()

columns = 19  # X
rows = 19  # Y
# Chance that the measurement gives the wrong color
# Here 40%, very high value, still converges with enough measurements
measure_uncertainty = 0.0
# Given a Measurement, how likely you are on the:
right_color = 1-measure_uncertainty
wrong_color = measure_uncertainty
speed = 0.03  # the lower the faster is movement (Simple sleep function)


class LastMovement(Enum):
    NONE = 0
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4


lastMovement = LastMovement(LastMovement.NONE)


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
        # A-Priori
        for column in range(rows):
            for row in range(columns):
                # Given Measurement, how likely that measure is wrong/right
                right = 0.95
                wrong = 0.05
                if(self.cells[column][row].color == measurement):
                    new_probs[column][row] = self.cells[column][row].probability * right
                else:
                    new_probs[column][row] = self.cells[column][row].probability * wrong
        # Calc normalizer + A-posteriori
        new_probs = np.dot(new_probs, 1/np.sum(new_probs))
        for row in range(rows):
            for column in range(columns):
                self.cells[column][row].probability = new_probs[column][row]


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

    def shift_and_blur(self, blur_around_x, blur_around_y, blur_radius, grid, lastMove):
        # Shift
        current_probabilities = np.zeros((columns, rows))
        shifted_probabilities = np.zeros((columns, rows))
        for row in range(rows):
            for column in range(columns):
                current_probabilities[column][row] = grid.cells[column][row].probability
        if(lastMove == LastMovement.LEFT):
            shifted_probabilities = np.roll(current_probabilities, -1, axis=0)
        if(lastMove == LastMovement.RIGHT):
            shifted_probabilities = np.roll(current_probabilities, 1, axis=0)
        if(lastMove == LastMovement.UP):
            shifted_probabilities = np.roll(current_probabilities, -1, axis=1)
        if(lastMove == LastMovement.DOWN):
            shifted_probabilities = np.roll(current_probabilities, 1, axis=1)

        for row in range(rows):
            for column in range(columns):
                grid.cells[column][row].probability = shifted_probabilities[column][row]

        # Blur all
        for row in range(rows):
            for column in range(columns):
                grid.cells[column][row].probability = grid.cells[column][row].probability * 0.7

    def move_player(self, grid):
        moved = False
        lastMovement = LastMovement.NONE
        keys = pygame.key.get_pressed()
        if(keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_UP] or keys[pygame.K_DOWN]):
            moved = True
            if keys[pygame.K_LEFT]:
                lastMovement = LastMovement.LEFT
                self.grid_x -= 1
                if(self.grid_x < 1):
                    self.grid_x = columns
            elif keys[pygame.K_RIGHT]:
                lastMovement = LastMovement.RIGHT
                self.grid_x += 1
                if(self.grid_x > columns):
                    self.grid_x = 1
            elif keys[pygame.K_UP]:
                lastMovement = LastMovement.UP
                self.grid_y -= 1
                if(self.grid_y < 1):
                    self.grid_y = rows
            elif keys[pygame.K_DOWN]:
                lastMovement = LastMovement.DOWN
                self.grid_y += 1
                if(self.grid_y > rows):
                    self.grid_y = 1
        self.update_rect()
        if(not moved):
            lastMovement = LastMovement.NONE
        if(moved):
            self.shift_and_blur(blur_around_x=(self.grid_x-1),
                                blur_around_y=(self.grid_y-1), blur_radius=2, grid=grid, lastMove=lastMovement)
        return moved

    def update_rect(self):
        self.x = grid.get_grid_x(self.grid_x)+round((grid.size-self.size)/2)
        self.y = grid.get_grid_y(self.grid_y)+round((grid.size-self.size)/2)
        self.rect = (self.x, self.y, self.size, self.size)


pygame.font.init()
font = pygame.font.SysFont(None, 25)
text_offset = 10


def real_position_display(screen, player):
    real_position_text = font.render(
        "True position: x: "+str(player.grid_x-1)+", y: "+str(player.grid_y-1), True, Color.Blue.value)
    screen.blit_text(real_position_text, (screen.width-screen.text_width+text_offset,
                                          text_offset, 100, 100))


def most_likely_position_display(screen, grid):
    probabilities = np.zeros((columns, rows))
    for row in range(rows):
        for column in range(columns):
            probabilities[column][row] = grid.cells[column][row].probability
    maxElement = np.amax(probabilities)
    grid_position = np.unravel_index(
        np.argmax(probabilities, axis=None), probabilities.shape)
    estimated_position_text = font.render(
        "Estimated position: x: "+str(grid_position[0])+", y: "+str(grid_position[1]), True, Color.Green.value)
    screen.blit_text(estimated_position_text, (screen.width-screen.text_width+text_offset,
                                               text_offset+100, 100, 100))


screen = Graphic(800, 800, "Bayes Filter")
grid = Grid(columns, rows, 37, 5)

init_x = random.randint(1, columns)
init_y = random.randint(1, rows)
player = Player(grid, init_x, init_y, 15, Color.Blue.value)


run = True
while run:

    # Set Background
    screen.get_background()
    # Draw Cells
    grid.draw_cells(screen)
    # Draw Player
   # player.draw_player(screen)
    # Speed
    time.sleep(speed)
    # Player moves
    moved = player.move_player(grid)

    if(moved):
        color = grid.measure_color(
            player.grid_x, player.grid_y, measure_uncertainty)
        grid.algorithm(color)
    # Display position of what the Filter "thinks" where the real position might be
    most_likely_position_display(screen, grid)
    # Display real position
    real_position_display(screen, player)
    # Refresh
    screen.update_screen()
    # Exit Condition
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


pygame.quit()
