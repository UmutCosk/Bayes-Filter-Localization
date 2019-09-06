import pygame
from graphics import Graphics
from car import Car
pygame.init()

window = Graphics(width=500, height=500)
car = Car(x_start=50, y_start=50, width=4, height=6, color=(255, 0, 0))

run = True
while run:

    # Draw the car on window
    window.draw(object=car)

    # Exit Condition
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    # Refresh-Rate
    pygame.time.delay(60)

pygame.quit()
