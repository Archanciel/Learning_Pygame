import turtle
from time import sleep

wn = turtle.Screen()
wn.bgcolor("black")
wn.title("Bouncing ball physics")
wn.tracer()
wn.setup(width=600, height=600)

ball = turtle.Turtle()
ball.shape("circle")
ball.color("green")
ball.penup()
ball.speed(0)
ball.dx = 0
ball.dy = 2.1


gravity = 0.1

while True:
	wn.update()
	#sleep(0.2)
	ball.dy -= gravity
	print("ycor ", ball.ycor(), " dy ", ball.dy)
	ball.sety(ball.ycor() + ball.dy)
	ball.setx(ball.xcor() + ball.dx)


	if ball.xcor() > 300:
		ball.dx *= -1
		
	if ball.xcor() < -300:
		ball.dx *= -1
		
	if ball.ycor() > 300:
		ball.dy *= -1
		
	if ball.ycor() < -300:
		ball.dy *= -1
