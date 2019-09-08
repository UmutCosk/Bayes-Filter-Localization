from graphics import ColorTypes
from enum import Enum


class CollisionSpot(Enum):
    NONE = 0
    LEFT = 1
    RIGHT = 2
    TOP = 3
    BOTTOM = 4


class Rect:
    def __init__(self, width, height, x, y):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.boundries = (self.x, self.y, self.width, self.height)

    def update_rect(self, x, y):
        self.x = x
        self.y = y
        self.boundries = (self.x, self.y, self.width, self.height)
        return self

    def get_rect(self):
        return self.boundries

    def get_center(self):
        x_center = self.x+self.width/2
        y_center = self.y+self.height/2
        return (x_center, y_center)

    def get_left_bound(self):
        x_center, y_center = self.get_center()
        return int(x_center - self.width/2)

    def get_right_bound(self):
        x_center, y_center = self.get_center()
        return int(x_center + self.width/2)

    def get_top_bound(self):
        x_center, y_center = self.get_center()
        return int(y_center - self.height/2)

    def get_bottom_bound(self):
        x_center, y_center = self.get_center()
        return int(y_center + self.height/2)

    def overlap_rect(self, other):
        collision_spot = CollisionSpot.NONE
        if(self.get_left_bound() < other.get_right_bound()):
            collision_spot = CollisionSpot.LEFT
        if(self.get_right_bound() > other.get_left_bound()):
            collision_spot = CollisionSpot.RIGHT
        if(self.get_top_bound() < other.get_bottom_bound()):
            collision_spot = CollisionSpot.TOP
        if(self.get_bottom_bound() > other.get_top_bound()):
            collision_spot = CollisionSpot.BOTTOM
        return collision_spot

    def colliding_wall(self, collision_spot, map_layout):
        coliding = False
        collision_offset = 1
        if(collision_spot == CollisionSpot.LEFT):
            if(tuple(map_layout[self.get_left_bound(), self.y]) == ColorTypes.Wall.value):
                coliding = True
        if(collision_spot == CollisionSpot.RIGHT):
            if(tuple(map_layout[self.get_right_bound(), self.y]) == ColorTypes.Wall.value):
                coliding = True
        if(collision_spot == CollisionSpot.TOP):
            if(tuple(map_layout[self.x, self.get_top_bound()]) == ColorTypes.Wall.value):
                coliding = True
        if(collision_spot == CollisionSpot.BOTTOM):
            if(tuple(map_layout[self.x, self.get_bottom_bound()]) == ColorTypes.Wall.value):
                coliding = True
        return coliding
