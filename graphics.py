import pygame


class Graphics:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Bayers Simulator")
        self.back_ground = Background('map.png', [0, 0])

    def draw_object(self, object):
        pygame.draw.rect(self.window, object.color, object.get_rect())

    def draw_area(self, color, rect):
        pygame.draw.rect(self.window, color, rect)

    def draw_pixels(self, image):
        for y_pixel in range(600):
            for x_pixel in range(800):
                rect = (x_pixel, y_pixel, 1, 1)
                color_value = image[y_pixel, x_pixel]
                color = (color_value, color_value, color_value)
                pygame.draw.rect(self.window, color, rect)

    def get_background(self):
        self.window.fill((175, 175, 175))
        self.window.blit(self.back_ground.image, self.back_ground.rect)

    def update_window(self):
        pygame.display.update()
        pygame.time.delay(1)  # ~60/17 Hz


class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
