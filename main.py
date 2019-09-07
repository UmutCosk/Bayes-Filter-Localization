# from __future__ import annotations  # type annotations
# import typing
import pygame
from graphics import Graphics
from car import Car
import time
import text
pygame.init()

# Init
screen = Graphics(width=800, text_width=400, height=600,
                  screen_name="Bayes Simulator", map_path="map.png")
car = Car(x_start=50, y_start=50, width=10, height=10,
          color=(255, 0, 0), velocity=3)

run = True
while run:
    # Set Background
    screen.get_background()
    # Car movement
    car.move(screen.width, screen.height, screen.map_layout)
    # Display Car position
    text.position_display(screen, car)
    # Draw the car on screen
    screen.draw_object(object=car)

    # Exit Condition
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    # Refresh-Rate @ 60Hz
    screen.update_screen()


pygame.quit()
