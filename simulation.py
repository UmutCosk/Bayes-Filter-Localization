# from __future__ import annotations  # type annotations
# import typing
import pygame
import cv2
import numpy as np
from graphics import Graphics
from graphics import Background
from car import Car
pygame.init()

# Init
window = Graphics(width=800, height=600)
car = Car(x_start=50, y_start=50, width=10, height=10,
          color=(255, 0, 0), velocity=1)

# Load Map Layout (Walls)
map_layout = cv2.imread("map.png")
map_layout = cv2.cvtColor(map_layout, cv2.COLOR_BGR2GRAY)

run = True
while run:
    # Set Background
    window.get_background()
    # Car movement
    car.move(window.width, window.height, map_layout)
    # Draw the car on window
    window.draw_object(object=car)

    # Exit Condition
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    # Refresh-Rate @ 60Hz
    window.update_window()


pygame.quit()
