import pygame
from graphics import Graphics
pygame.font.init()

font = pygame.font.SysFont(None, 25)

text_offset = 10


def position_display(screen, car):
    position_text = font.render(
        "Car position: x: "+str(car.x)+", y: "+str(car.y), True, (0, 0, 255))
    screen.blit_text(position_text, (screen.width-screen.text_width+text_offset,
                                     text_offset, 100, 100))
