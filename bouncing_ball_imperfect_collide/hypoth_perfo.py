import timeit
import math

x1 = 20
x2 = 140
y1 = 30
y2 = 110
loop = 1000

def loop_hypot():
	for i in range(loop):
		x = x2 - x1
		y = y2 - y1
		h = math.hypot(x,y)
	
print('hypot:')
print(timeit.timeit(loop_hypot, number=loop))

def loop_square_hypot():
	for i in range(loop):
		x = x2 - x1
		y = y2 - y1
		hs = x * x + y * y
	

print('square hypot:')
print(timeit.timeit(loop_square_hypot, number=loop))

