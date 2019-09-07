import pygame
import cv2


class Graphics:
    def __init__(self, width, text_width, height, screen_name, map_path):
        self.width = width+400
        self.text_width = text_width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(screen_name)

        # Load Map Layout (Walls)
        map_layout = cv2.imread(map_path)
        self.map_layout = cv2.cvtColor(map_layout, cv2.COLOR_BGR2GRAY)
        self.back_ground = Background(map_path, [0, 0])

    def draw_object(self, object):
        pygame.draw.rect(self.screen, object.color, object.get_rect())

    def draw_area(self, color, rect):
        pygame.draw.rect(self.screen, color, rect)

    def draw_pixels(self, image):
        for y_pixel in range(600):
            for x_pixel in range(800):
                rect = (x_pixel, y_pixel, 1, 1)
                color_value = image[y_pixel, x_pixel]
                color = (color_value, color_value, color_value)
                pygame.draw.rect(self.screen, color, rect)

    def get_background(self):
        self.screen.fill((175, 175, 175))
        self.screen.blit(self.back_ground.image, self.back_ground.rect)

    def update_screen(self):
        pygame.display.update()
        pygame.time.delay(1)  # ~60/17 Hz

    def blit_text(self, text, rect):
        self.screen.blit(text, rect)


class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
