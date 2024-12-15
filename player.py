import math
import turtle

class Player:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.speed = 0
        self.angle = 0
        self.turtle = turtle.Turtle()
        self.turtle.shape("circle")
        self.turtle.color(self.color)
        self.turtle.penup()
        self.turtle.goto(self.x, self.y)

    def set_direction(self, angle, speed):
        self.angle = angle
        self.speed = speed

    def move(self):
        if self.speed > 0:
            radian = math.radians(self.angle)
            self.x += math.cos(radian) * self.speed
            self.y += math.sin(radian) * self.speed
            self.speed *= 0.95  # Friction to slow down
            self.turtle.goto(self.x, self.y)

    def is_moving(self):
        return self.speed > 0.1

    def get_angle_to_position(self, x, y):
        return math.degrees(math.atan2(y - self.y, x - self.x))

    def get_distance_to_position(self, x, y):
        return math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)