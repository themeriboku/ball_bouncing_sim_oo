import turtle
import math
from paddle import Paddle
from Soccerball import SoccerBall
from arrow import Arrow
from player import Player

class SoccerGame:
    def __init__(self):
        self.screen = turtle.Screen()
        self.screen.title("Soccer Game")
        self.screen.bgcolor("green")
        self.screen.setup(width=1000, height=800)
        self.screen.tracer(0)

        self.goalkeeper1_turtle = turtle.Turtle()
        self.goalkeeper2_turtle = turtle.Turtle()
        self.goalkeeper1 = Paddle(width=10, height=100, color="red", my_turtle=self.goalkeeper1_turtle)
        self.goalkeeper2 = Paddle(width=0, height=100, color="blue", my_turtle=self.goalkeeper2_turtle)
        self.player1 = Player(-350, 0, color="blue")
        self.player2 = Player(350, 0, color="red")
        self.ball = SoccerBall(0, 0, id=1)
        self.arrow = Arrow()
        self.scoreboard = turtle.Turtle()
        self.score = {"player1": 0, "player2": 0}
        self.current_player = self.player1
        self.player_moving = False
        self.turn_ended = False
        self.arrow_active = False

        self.setup_field()
        self.setup_goalkeepers()
        self.setup_scoreboard()
        self.bind_events()
        self.start_game()

    def setup_field(self):
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

    def setup_goalkeepers(self):
        self.goalkeeper1_turtle.shape("square")
        self.goalkeeper1_turtle.penup()
        self.goalkeeper2_turtle.shape("square")
        self.goalkeeper2_turtle.penup()

        self.goalkeeper1.set_location([400, 0])  # Right side of the field
        self.goalkeeper2.set_location([-400, 0])  # Left side of the field

        self.goalkeeper1.draw()
        self.goalkeeper2.draw()

    def setup_scoreboard(self):
        self.scoreboard.hideturtle()
        self.scoreboard.color("white")
        self.scoreboard.penup()
        self.scoreboard.goto(0, 350)
        self.update_score()

    def update_score(self):
        self.scoreboard.clear()
        self.scoreboard.write(
            f"Player 1: {self.score['player1']}  Player 2: {self.score['player2']}",
            align="center",
            font=("Courier", 24, "normal")
        )

    def check_goal(self):
        if self.ball.x < -500:  # Left goal
            self.score["player2"] += 1
            self.reset_positions()
            self.update_score()
            self.turn_ended = True

        if self.ball.x > 500:  # Right goal
            self.score["player1"] += 1
            self.reset_positions()
            self.update_score()
            self.turn_ended = True

        # Check for win condition
        if self.score["player1"] == 5:
            self.end_game("Player 1 Wins!")
        elif self.score["player2"] == 5:
            self.end_game("Player 2 Wins!")

    def end_game(self, message):
        self.scoreboard.goto(0, 0)
        self.scoreboard.write(message, align="center", font=("Courier", 36, "normal"))
        self.ball.vx = self.ball.vy = 0  # Stop ball movement
        self.screen.update()
        self.screen.bye()  # Close the turtle graphics window

    def reset_positions(self):
        self.player1.x, self.player1.y = -350, 0
        self.player2.x, self.player2.y = 350, 0
        self.ball.x, self.ball.y = 0, 0
        self.ball.vx, self.ball.vy = 0, 0
        self.player1.turtle.goto(self.player1.x, self.player1.y)
        self.player2.turtle.goto(self.player2.x, self.player2.y)
        self.ball.turtle.goto(self.ball.x, self.ball.y)

    def switch_turn(self):
        self.current_player = self.player2 if self.current_player == self.player1 else self.player1

    def drag_player(self, x, y):
        angle = self.current_player.get_angle_to_position(x, y)
        distance = self.current_player.get_distance_to_position(x, y)
        distance = min(distance, 50)  # Cap the distance at 50
        self.arrow.update(self.current_player.x, self.current_player.y, angle, distance)
        self.arrow_active = True

    def release_player(self, x, y):
        if self.arrow_active:
            angle = self.current_player.get_angle_to_position(x, y)
            distance = self.current_player.get_distance_to_position(x, y)
            speed = min(distance / 10, 15)  # Scale speed by drag distance with a cap
            self.current_player.set_direction(angle, speed)
            self.arrow.turtle.clear()
            self.player_moving = True
            self.arrow_active = False

    def bind_events(self):
        self.screen.listen()
        self.screen.onscreenclick(self.release_player)
        self.screen.ontimer(lambda: self.current_player.turtle.ondrag(self.drag_player), 100)

    def start_game(self):
        self.ball.draw()
        self.game_loop()
        self.screen.mainloop()

    def game_loop(self):
        if self.player_moving:
            self.current_player.move()
            if not self.current_player.is_moving():
                self.player_moving = False
                self.turn_ended = True  # Indicate that the player's turn has ended

        if self.ball.is_moving():
            self.ball.move()  # The ball will move and update its position automatically
            self.ball.check_collision(self.player1)
            self.ball.check_collision(self.player2)
            self.check_goal()

        if self.turn_ended:
            self.switch_turn()
            self.turn_ended = False

        self.screen.update()
        self.screen.ontimer(self.game_loop, 20)

# Start the game
if __name__ == "__main__":
    game = SoccerGame()
