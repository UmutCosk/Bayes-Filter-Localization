import numpy as np
import math
import time


class BayesFilter:
    def __init__(self, grid_width, grid_height, x0, y0):
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.slots_proberbility = []
        self.radius = 50
        probability = 1 / (grid_width*grid_height)
        for i in range(grid_width):
            for j in range(grid_height):
                self.slots_proberbility.append(probability)
        self.lastPostion = (x0, y0)
        self.slots_proberbility[self.get_1D_index(x0, y0)] = 3000
        self.normalize_probability()

    def set_priori_position(self, x_moved, y_moved):
        self.lastPostion = (x_moved, y_moved)
        self.slots_proberbility[self.get_1D_index(x_moved, y_moved)] = 0.9

    def get_1D_index(self, x, y):
        return y*self.grid_width+x

    def get_best_probability(self):
        maxElement = np.amax(self.slots_proberbility)
        return maxElement

    def get_likeliest_index(self):
        maxValue = np.amax(self.slots_proberbility)
        result = np.where(self.slots_proberbility == maxValue)
        return result

    def normalize_probability(self):
        sum_probability = np.sum(self.slots_proberbility)
        for i in range(len(self.slots_proberbility)):
            self.slots_proberbility[i] = self.slots_proberbility[i] / \
                sum_probability

    def flaten_probability(self):
        flaten_magnitude = 0.0001
        for i in range(len(self.slots_proberbility)):
            self.slots_proberbility[i] += flaten_magnitude
        self.normalize_probability()

    def flaten_around(self, x, y):
        flaten_magnitude = 0.1
        for j in range(self.radius):
            for i in range(self.radius):
                self.slots_proberbility[self.get_1D_index(
                    x+i, y+j)] = self.slots_proberbility[self.get_1D_index(x+i, y+j)] + flaten_magnitude
            for i in range(self.radius):
                self.slots_proberbility[self.get_1D_index(
                    x-i, y+j)] = self.slots_proberbility[self.get_1D_index(x-i, y+j)] + flaten_magnitude
            for i in range(self.radius):
                self.slots_proberbility[self.get_1D_index(
                    x+i, y-j)] = self.slots_proberbility[self.get_1D_index(x+i, y-j)] + flaten_magnitude
            for i in range(self.radius):
                self.slots_proberbility[self.get_1D_index(
                    x-i, y-j)] = self.slots_proberbility[self.get_1D_index(x-i, y-j)] + flaten_magnitude
        self.normalize_probability()
