import pygame
from graphics import Graphics
from car import Car
pygame.init()

window = Graphics(width=800, height=600)
car = Car(x_start=50, y_start=50, width=20, height=35,
          color=(255, 0, 0), velocity=10)

run = True
while run:

    # Car movement
    car.move(window)
    # Draw the car on window
    window.draw(object=car)
    # Exit Condition
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    # Refresh-Rate
    pygame.time.delay(17)  # ~60Hz

pygame.quit()
