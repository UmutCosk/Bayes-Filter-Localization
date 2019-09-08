
from graphic import Graphic
from rect import Rect


class Landmark:
    def __init__(self, x, y, size, color):
        self.x = x
        self.y = y
        self.rect = Rect(size, size, self.x, self.y)
        self.color = color
