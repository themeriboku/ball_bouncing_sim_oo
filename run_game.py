import turtle
import math
from paddle import Paddle
from Soccerball import SoccerBall
from arrow import Arrow
from player import Player

screen = turtle.Screen()
screen.title("Soccer Game")
screen.bgcolor("green")
screen.setup(width=1000, height=800)
screen.tracer(0)

# Draw field
def draw_field():
    drawer = turtle.Turtle()
    drawer.hideturtle()
    drawer.color("white")
    drawer.penup()

    # Main field
    drawer.goto(-400, -300)
    drawer.pendown()
    for _ in range(2):
        drawer.forward(800)
        drawer.left(90)
        drawer.forward(600)
        drawer.left(90)

    # Goal zones
    # Left goal zone
    drawer.penup()
    drawer.goto(-500, -100)
    drawer.pendown()
    drawer.goto(-400, -100)
    drawer.goto(-400, 100)
    drawer.goto(-500, 100)
    drawer.goto(-500, -100)

    # Right goal zone
    drawer.penup()
    drawer.goto(400, -100)
    drawer.pendown()
    drawer.goto(500, -100)
    drawer.goto(500, 100)
    drawer.goto(400, 100)
    drawer.goto(400, -100)

    # Center line
    drawer.penup()
    drawer.goto(0, -300)
    drawer.pendown()
    drawer.goto(0, 300)

draw_field()

goalkeeper1_turtle = turtle.Turtle()
goalkeeper1_turtle.shape("square")
goalkeeper1_turtle.penup()

goalkeeper2_turtle = turtle.Turtle()
goalkeeper2_turtle.shape("square")
goalkeeper2_turtle.penup()

# Create two goalkeepers
goalkeeper1 = Paddle(width=20, height=100, color="red", my_turtle=goalkeeper1_turtle)
goalkeeper2 = Paddle(width=20, height=100, color="blue", my_turtle=goalkeeper2_turtle)

# Set their initial positions
goalkeeper1.set_location([400, 0])  # Right side of the field
goalkeeper2.set_location([-400, 0])  # Left side of the field

# Draw the goalkeepers
goalkeeper1.draw()
goalkeeper2.draw()

# Create objects
player1 = Player(-350, 0, color="blue")
player2 = Player(350, 0, color="red")
ball = SoccerBall(0, 0, id=1)
ball.draw()
arrow = Arrow()

# Game state
current_player = player1
player_moving = False
turn_ended = False
arrow_active = False
score = {"player1": 0, "player2": 0}

# Scoreboard
scoreboard = turtle.Turtle()
scoreboard.hideturtle()
scoreboard.color("white")
scoreboard.penup()
scoreboard.goto(0, 350)
scoreboard.write("Player 1: 0  Player 2: 0", align="center", font=("Courier", 24, "normal"))

def update_score():
    """Update the scoreboard display."""
    scoreboard.clear()
    scoreboard.write(
        f"Player 1: {score['player1']}  Player 2: {score['player2']}",
        align="center",
        font=("Courier", 24, "normal"),
    )

def check_goal():
    """Check if the ball enters a goal zone and update the score."""
    global turn_ended
    if ball.x < -500:  # Left goal
        score["player2"] += 1
        reset_positions()
        update_score()
        turn_ended = True

    if ball.x > 500:  # Right goal
        score["player1"] += 1
        reset_positions()
        update_score()
        turn_ended = True

    # Check for win condition
    if score["player1"] == 5:
        end_game("Player 1 Wins!")
    elif score["player2"] == 5:
        end_game("Player 2 Wins!")

def end_game(message):
    """End the game and display the winner."""
    scoreboard.goto(0, 0)
    scoreboard.write(message, align="center", font=("Courier", 36, "normal"))
    ball.vx = ball.vy = 0  # Stop ball movement
    screen.update()
    screen.bye()  # Close the turtle graphics window

def reset_positions():
    """Reset player and ball positions."""
    player1.x, player1.y = -350, 0
    player2.x, player2.y = 350, 0
    ball.x, ball.y = 0, 0
    ball.vx, ball.vy = 0, 0
    player1.turtle.goto(player1.x, player1.y)
    player2.turtle.goto(player2.x, player2.y)
    ball.turtle.goto(ball.x, ball.y)

def switch_turn():
    """Switch turn to the other player."""
    global current_player
    current_player = player2 if current_player == player1 else player1

# Dragging sets up arrow but does not move player
def drag_player(x, y):
    global arrow_active
    angle = current_player.get_angle_to_position(x, y)
    distance = current_player.get_distance_to_position(x, y)
    distance = min(distance, 50)  # Cap the distance at 50
    arrow.update(current_player.x, current_player.y, angle, distance)
    arrow_active = True

# Release triggers player movement
def release_player(x, y):
    global player_moving, arrow_active
    if arrow_active:
        angle = current_player.get_angle_to_position(x, y)
        distance = current_player.get_distance_to_position(x, y)
        speed = min(distance / 10, 15)  # Scale speed by drag distance with a cap
        current_player.set_direction(angle, speed)
        arrow.turtle.clear()
        player_moving = True
        arrow_active = False

# Mouse bindings
screen.listen()
screen.onscreenclick(release_player)
screen.ontimer(lambda: current_player.turtle.ondrag(drag_player), 100)

# Main game loop
def game_loop():
    global player_moving, turn_ended

    if player_moving:
        current_player.move()
        if not current_player.is_moving():
            player_moving = False
            turn_ended = True  # Indicate that the player's turn has ended

    if ball.is_moving():
        ball.move()  # The ball will move and update its position automatically
        ball.check_collision(player1)
        ball.check_collision(player2)
        check_goal()

    if turn_ended:
        switch_turn()
        turn_ended = False

    screen.update()
    screen.ontimer(game_loop, 20)

game_loop()
screen.mainloop()