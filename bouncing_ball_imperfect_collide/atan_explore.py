import math

dy = -3
dx = 3
print('dx: ', dx, ' dy: ', dy)
a = math.atan2(dy, dx)
print(a)
print(math.degrees(a))

dy = -3
dx = -3
print('dx: ', dx, ' dy: ', dy)
a = math.atan2(dy, dx)
print(a)
print(math.degrees(a))

dy = 3
dx = 3
print('dx: ', dx, ' dy: ', dy)
a = math.atan2(dy, dx)
print(a)
print(math.degrees(a))

dy = 3
dx = -3
print('dx: ', dx, ' dy: ', dy)
a = math.atan2(dy, dx)
print(a)
print(math.degrees(a))