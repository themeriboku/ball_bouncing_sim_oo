import turtle
class Arrow:
    def __init__(self):
        self.turtle = turtle.Turtle()
        self.turtle.hideturtle()
        self.turtle.color("black")
        self.turtle.penup()

    def update(self, x, y, angle, length):
        self.turtle.clear()
        self.turtle.penup()
        self.turtle.goto(x, y)
        self.turtle.setheading(angle)
        self.turtle.pendown()
        self.turtle.forward(length)
        self.turtle.penup()

