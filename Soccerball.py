from ball import Ball
import math
import turtle

class SoccerBall(Ball):
    def __init__(self, x, y, id):
        super().__init__(size=10, x=x, y=y, vx=0, vy=0, color="white", id=id)
        self.turtle = turtle.Turtle()  # Initialize turtle object
        self.turtle.shape("circle")  # Set the shape to a circle (ball)
        self.turtle.color(self.color)  # Set color to match the ball's color
        self.turtle.penup()  # Don't draw lines
        self.turtle.goto(self.x, self.y)

    def move(self):
        super().move()
        # Boundary collision
        if self.x < -400 or self.x > 400:
            self.bounce_off_vertical_wall()
        if self.y < -300 or self.y > 300:
            self.bounce_off_horizontal_wall()

        # Friction
        self.vx *= 0.98
        self.vy *= 0.98

    def check_collision(self, player):
        distance = self.distance(player)
        if distance < 20:  # Assuming both ball and player are of radius ~10
            angle = player.get_angle_to_position(self.x, self.y)
            radian = math.radians(angle)
            self.vx = math.cos(radian) * player.speed
            self.vy = math.sin(radian) * player.speed
    
    def is_moving(self):
        # A simple check to see if the ball has any velocity
        return self.vx != 0 or self.vy != 0

    def draw(self):
        # Draw the ball initially at the given position
        self.turtle.goto(self.x, self.y)

