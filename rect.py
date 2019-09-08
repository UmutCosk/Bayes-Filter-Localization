from graphic import ColorTypes
from enum import Enum


class CollisionSpot(Enum):
    NONE = 0
    LEFT = 1
    RIGHT = 2
    TOP = 3
    BOTTOM = 4


class Rect():
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
        return (int(x_center), int(y_center))

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

    # def intersecting(self, other):
    #     intersecting = False
    #     if(self.get_right_bound() > other.get_left_bound() and self.get_right_bound() < other.get_right_bound()):
    #         if(self.get_top_bound() < other.get_bottom_bound() and self.get_top_bound() > other.get_top_bound()):
    #             intersecting = True
    #     if(self.get_left_bound() < other.get_right_bound() and self.get_left_bound() > other.get_left_bound()):
    #         if(self.get_top_bound() < other.get_bottom_bound() and self.get_top_bound() > other.get_top_bound()):
    #             intersecting = True
    #     if(self.get_left_bound() < other.get_right_bound() and self.get_left_bound() > other.get_left_bound()):
    #         if(self.get_bottom_bound() > other.get_top_bound() and self.get_bottom_bound() < other.get_bottom_bound()):
    #             intersecting = True
    #     if(self.get_right_bound() > other.get_left_bound() and self.get_right_bound() < other.get_right_bound()):
    #         if(self.get_bottom_bound() > other.get_top_bound() and self.get_bottom_bound() < other.get_bottom_bound()):
    #             intersecting = True
    #     return intersecting

    # def get_top_left_corner(self):
    #     return (self.x, self.y)

    # def get_top_right_corner(self):
    #     return (self.x+self.width, self.y)

    # def get_bottom_right_corner(self):
    #     return (self.x+self.width, self.y+self.height)

    # def get_bottom_left_corner(self):
    #     return (self.x, self.y+self.height)

    def colliding_other(self, car, other):
        if(car.currentCollision == CollisionSpot.NONE):
            if(self.get_right_bound() < other.get_left_bound() and self.intersecting(other)):
                car.currentCollision = CollisionSpot.RIGHT
            if(self.get_right_bound() > other.get_left_bound() and self.intersecting(other)):
                car.currentCollision = CollisionSpot.LEFT
            if(self.get_top_bound() < other.get_bottom_bound() and self.intersecting(other)):
                car.currentCollision = CollisionSpot.BOTTOM
            if(self.get_bottom_bound() > other.get_top_bound() and self.intersecting(other)):
                car.currentCollision = CollisionSpot.TOP

    def colliding_wall(self, car, map_layout):
        if(car.currentCollision == CollisionSpot.NONE):
            collision_offset = 1
            map_value = tuple(
                map_layout[self.get_left_bound(), self.y+round(self.height/2)])
            if(map_value == ColorTypes.Wall.value):
                car.currentCollision = CollisionSpot.LEFT
            map_value = tuple(
                map_layout[self.get_right_bound(), self.y+round(self.height/2)])
            if(map_value == ColorTypes.Wall.value):
                car.currentCollision = CollisionSpot.RIGHT
            map_value = tuple(
                map_layout[self.x+round(self.width/2), self.get_top_bound()])
            if(map_value == ColorTypes.Wall.value):
                car.currentCollision = CollisionSpot.TOP
            map_value = tuple(
                map_layout[self.x+round(self.width/2), self.get_bottom_bound()])
            if(map_value == ColorTypes.Wall.value):
                car.currentCollision = CollisionSpot.BOTTOM
