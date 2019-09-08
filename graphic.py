import pygame
import cv2
import numpy as np
from enum import Enum

refresh_rate = 1


class Color(Enum):
    Red = (255, 0, 0)
    Green = (0, 175, 0)  # Darker Green
    Blue = (0, 0, 255)
    Yellow = (0, 255, 255)
    Black = (0, 0, 0)
    Gray1 = (175, 175, 175)


class ColorTypes(Enum):
    Wall = Color.Black.value
    Landmark = Color.Green.value


class Graphic:
    def __init__(self, width, height, screen_name, map_path):
        self.text_width = round(width/2)
        self.width = width + self.text_width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(screen_name)

        # Load Map Layout (Walls)
        self.map_layout = cv2.imread(map_path)
        # Swaps axis to have x,y order
        self.map_layout = np.swapaxes(self.map_layout, 1, 0)
        self.back_ground = Background(map_path, [0, 0])

    def draw_object(self, object_color, object_rect):
        pygame.draw.rect(self.screen,  object_color, object_rect.get_rect())

    def draw_area(self, color, rect):
        pygame.draw.rect(self.screen, color, rect)

    def get_background(self):
        self.screen.fill(Color.Gray1.value)
        self.screen.blit(self.back_ground.image, self.back_ground.rect)

    def update_screen(self):
        pygame.display.update()
        pygame.time.delay(refresh_rate)  # ~60/17 Hz

    def blit_text(self, text, rect):
        self.screen.blit(text, rect)

    def draw_circle(self, color, position, radius, width):
        pygame.draw.circle(self.screen, color, position, radius, width)


class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
