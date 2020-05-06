import turtle
from time import sleep

wn = turtle.Screen()
wn.bgcolor("black")
wn.title("Bouncing ball physics")
wn.tracer(0,0)
wn.setup(width=600, height=700)

ball = turtle.Turtle()
ball.shape("circle")
ball.color("green")
ball.penup()
ball.speed(0)
ball.dx = 0
ball.dy = 2.1


gravity = 0.4
previousSign = False
previousPreviousSign = False

while True:
	wn.update()
	ball.dy -= gravity
	currentSign = ball.dy > 0

	if currentSign != previousSign and currentSign == previousPreviousSign:
		# trying to fix ball flipping at end of rebound
		ball.dy = 2.1
		ball.sety(0)
	else:
		previousPreviousSign = previousSign
		previousSign = currentSign

	#print("ycor ", ball.ycor(), " dy ", ball.dy)
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

	sleep(0.02)