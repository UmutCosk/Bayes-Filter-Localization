import pygame
from graphic import Graphic
from graphic import Color
pygame.font.init()

font = pygame.font.SysFont(None, 25)

text_offset = 10


def position_display(screen, car):
    real_position_text = font.render(
        "Real position: x: "+str(car.x)+", y: "+str(car.y), True, Color.Blue.value)
    screen.blit_text(real_position_text, (screen.width-screen.text_width+text_offset,
                                          text_offset, 100, 100))
    estimated_position_text = font.render(
        "Estimated position: x: "+str(car.x)+", y: "+str(car.y), True, Color.Green.value)
    screen.blit_text(estimated_position_text, (screen.width-screen.text_width+text_offset,
                                               text_offset+100, 100, 100))
