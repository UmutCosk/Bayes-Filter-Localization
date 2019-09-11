import pygame
from graphic import Graphic
from graphic import Color
pygame.font.init()

font = pygame.font.SysFont(None, 25)

text_offset = 10


def real_position_display(screen, car):
    real_position_text = font.render(
        "Real position: x: "+str(car.x)+", y: "+str(car.y), True, Color.Blue.value)
    screen.blit_text(real_position_text, (screen.width-screen.text_width+text_offset,
                                          text_offset, 100, 100))


def estimated_position_display(screen, x_ext, y_est):
    estimated_position_text = font.render(
        "Estimated position: x: "+str(x_ext)+", y: "+str(y_est), True, Color.Green.value)
    screen.blit_text(estimated_position_text, (screen.width-screen.text_width+text_offset,
                                               text_offset+100, 100, 100))
