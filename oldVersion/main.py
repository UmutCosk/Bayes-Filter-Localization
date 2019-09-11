# from __future__ import annotations  # type annotations
# import typing
import pygame
from bayes import BayesFilter
from graphic import Graphic
from graphic import Color
from rect import CollisionSpot
from car import Car
from landmark import Landmark
import time
import text
pygame.init()

# Create Bayes Grid
bayes_filter = BayesFilter(800, 600, 50, 50)
# Create screen
screen = Graphic(width=800, height=600,
                 screen_name="Bayes Simulator", map_path="map.png")
# Create car
car = Car(x_start=50, y_start=50, width=10, height=10,
          color=Color.Blue.value, velocity=3, detection_radius=100)
# Create Landmarks
landmarks = []
landmarks_pos_x = [344, 626]
landmarks_pos_y = [314, 245]
for landmark_x, landmark_y in zip(landmarks_pos_x, landmarks_pos_y):
    landmarks.append(Landmark(landmark_x, landmark_y, 10, Color.Green.value))

dt = 0
update_rate = 1
run = True
update = False
while run:
    tic = time.time()
    if(dt > update_rate):
        dt = 0
        update = True

    # Set Background
    screen.get_background()
    # Display Car position
    text.real_position_display(screen, car)
    # Show detection area
    screen.draw_circle(
        Color.Red.value, car.rect.get_center(), car.detect_radius, 1)
    # Draw the car on screen
    screen.draw_object(car.color, car.rect)
    # Draw landmarks on screen
    for landmark in landmarks:
        screen.draw_object(landmark.color, landmark.rect)

    # -- Check for Collisions
    car.currentCollision = CollisionSpot.NONE
    # with Wall
    car.rect.colliding_wall(car, screen.map_layout)
    # with Landmarks
    # for landmark in landmarks:
    #     car.rect.colliding_other(car, landmark.rect)
    # Car movement
    update = car.move(screen.width, screen.height,
                      screen.map_layout, bayes_filter, update)
    # Exit Condition
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    # Refresh
    screen.update_screen()
    toc = time.time()
    dt += toc-tic

pygame.quit()
