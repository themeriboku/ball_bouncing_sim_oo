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
        self.mass = 100  

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
    
    def check_collision(self, other_player):
        # Calculate distance between the two players
        distance = math.sqrt((self.x - other_player.x)**2 + (self.y - other_player.y)**2)
        
        if distance < self.radius + other_player.radius:
            # Simple elastic collision response
            angle = math.atan2(self.y - other_player.y, self.x - other_player.x)
            self.vx, self.vy = -math.cos(angle) * self.speed, -math.sin(angle) * self.speed
            other_player.vx, other_player.vy = math.cos(angle) * other_player.speed, math.sin(angle) * other_player.speed

            # Adjust positions to avoid overlap
            overlap = self.radius + other_player.radius - distance
            self.x += math.cos(angle) * overlap / 2
            self.y += math.sin(angle) * overlap / 2
            other_player.x -= math.cos(angle) * overlap / 2
            other_player.y -= math.sin(angle) * overlap / 2
            self.turtle.goto(self.x, self.y)
            other_player.turtle.goto(other_player.x, other_player.y)