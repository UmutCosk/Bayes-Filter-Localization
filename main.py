# from __future__ import annotations  # type annotations
# import typing
from graphic import Graphic
from graphic import Color
import random
import pygame
import time
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

    def draw_cells(self, screen):
        for i in range(self.rows):
            for j in range(self.columns):
                alpha = 200 * self.cells[i][j].probability + 25
                screen.draw_area(
                    self.cells[i][j].color, self.cells[i][j].rect, alpha)

    def get_grid_x(self, x):
        return self.padding*x+self.size*(x-1)

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

    def measure_color(self, x, y):
        
        return self.cells[-4][-3].color


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
        return moved

    def update_rect(self):
        self.x = grid.get_grid_x(self.grid_x)+round((grid.size-self.size)/2)
        self.y = grid.get_grid_y(self.grid_y)+round((grid.size-self.size)/2)
        self.rect = (self.x, self.y, self.size, self.size)


# class BayesFilter:
#     def __init__(self, grid):
#         self.red_probability = grid.red_count/grid.size**2
#         self.green_probability = grid.green_count/grid.size**2
#         self.measure_certainty = 1
#         self.green_cells = []
#         self.red_cells = []
#         for cell in grid.cells:
#             if(cell.color == Color.Red.value):
#                 self.red_cells.append(cell)
#             else:
#                 self.green_cells.append(cell)

#     def algorithm(self, measurement):
#         total_red_probability = 0
#         total_green_probability = 0
#         red_faktor = 0
#         green_faktor = 0
#         # a-priori
#         if(measurement == Color.Red.value):
#             for red_cell in self.red_cells:
#                 red_faktor += red_cell.probability * self.measure_certainty
#             for green_cell in self.green_cells:
#                 green_faktor += green_cell.probability * \
#                     (1-self.measure_certainty)
#         if(measurement == Color.Green.value):
#             for red_cell in self.red_cells:
#                 red_faktor += red_cell.probability * (1-self.measure_certainty)
#             for green_cell in self.green_cells:
#                 green_faktor += green_cell.probability * \
#                     self.measure_certainty
#         print(green_faktor)
#         print(red_faktor)
#         # Calc normalizer mue
#         mue = 1 / (green_faktor + red_faktor)

#         # a-Posteriori
#         for i in range(len(self.red_cells)):
#             print(self.red_cells[i].probability)

#         for i in range(len(self.red_cells)):
#             if(measurement == Color.Red.value):
#                 self.red_cells[i].probability = self.red_cells[i].probability * \
#                     mue * self.measure_certainty
#             else:
#                 self.red_cells[i].probability = self.red_cells[i].probability * \
#                     mue * (1-self.measure_certainty)

#         for i in range(len(self.green_cells)):
#             if(measurement == Color.Green.value):
#                 self.green_cells[i].probability = self.green_cells[i].probability * \
#                     mue * self.measure_certainty
#             else:
#                 self.green_cells[i].probability = self.green_cells[i].probability * \
#                     mue * (1-self.measure_certainty)

        # for red_cell in self.red_cells:
        #     total_red_probability += red_cell.probability
        # for green_cell in self.green_cells:
        #     total_green_probability += green_cell.probability
        # # Conditional Probability
        # if(measurement == Color.Red.value):
        #     red_faktor = len(self.red_cells)*self.measure_certainty
        #     green_faktor = len(self.green_cells)*(1-self.measure_certainty)
        # else:
        #     red_faktor = len(self.red_cells)*(1-self.measure_certainty)
        #     green_faktor = len(self.green_cells)*self.measure_certainty
        # # Calculate normalize factor
        # mue = 1 / (total_red_probability*red_faktor +
        #            total_green_probability*green_faktor)
        # print(mue)
        # # a-posteriori
        # for i in range(len(self.red_cells)):
        #     if(measurement == Color.Red.value):
        #         self.red_cells[i].probability = self.red_cells[i].probability * \
        #             mue * (self.measure_certainty)
        #     else:
        #         self.red_cells[i].probability = self.red_cells[i].probability * \
        #             mue * (1-self.measure_certainty)
        # for i in range(len(self.green_cells)):
        #     if(measurement == Color.Green.value):
        #         self.green_cells[i].probability = self.green_cells[i].probability * \
        #             mue * (self.measure_certainty)
        #     else:
        #         self.green_cells[i].probability = self.green_cells[i].probability * \
        #             mue * (1-self.measure_certainty)


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

columns = 3 # X
rows = 8 # Y


screen = Graphic(800, 800, "Bayes Filter")
grid = Grid(columns, rows, 37, 5)

init_x = random.randint(1, columns)
init_y = random.randint(1, rows)
player = Player(grid, init_x, init_y, 15, Color.Blue.value)
# bayes_filter = BayesFilter(grid)


run = True
while run:
   
    # Set Background
    screen.get_background()
    # Draw Cells
    grid.draw_cells(screen)
    # Draw Player
    player.draw_player(screen)
  
    # Player moves
    moved = player.move_player(grid)
    #color = grid.measure_color(player.grid_x, player.grid_y)
           # bayes_filter.algorithm(color)
            # summe = 0
            # for cell in grid.cells:
            #     summe += cell.probability

    real_position_display(screen, player)
    # Refresh
    screen.update_screen()
    # Exit Condition
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


pygame.quit()
