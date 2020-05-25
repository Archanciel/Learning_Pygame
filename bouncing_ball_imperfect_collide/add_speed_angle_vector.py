import math

def addAngleSpeedVectorYAxisBased(vector1, vector2):
	print("Y axis based\n")
	x1 = math.sin(vector1[0]) * vector1[1]
	y1 = math.cos(vector1[0]) * vector1[1]
	
	x2 = math.sin(vector2[0]) * vector2[1]
	y2 = math.cos(vector2[0]) * vector2[1]
	
	xSum = x1 + x2
	ySum = y1 + y2
	speedSum = math.hypot(xSum, ySum)
	angleSum = (math.pi / 2) - math.atan2(ySum, xSum)
	print("angleSum pi/2 - atan2", math.degrees(angleSum))
	
	# alternative way of computing angleSum
	angleSum2 = math.acos(ySum / speedSum)
	print("angleSum acos ", math.degrees(angleSum2))
	
	# alternative way of computing angleSum
	angleSum3 = math.atan(xSum / ySum)
	print("angleSum atan ", math.degrees(angleSum3))
	
	return (angleSum, speedSum)

		
def addAngleSpeedVectorXAxisBased(vector1, vector2):
	angle1 = vector1[0]
	length1 = vector1[1]		
	angle2 = vector2[0]
	length2 = vector2[1]		
		
	x = math.cos(angle1) * length1 + math.cos(angle2) * length2
	y = math.sin(angle1) * length1 + math.sin(angle2) * length2
		
	length = math.hypot(x, y)
	angle = math.atan2(y, x)
		
	return (angle, length)
			
if __name__ == "__main__":
	vec1 = (math.radians(30), 8.06)
	vec2 = (math.radians(120), 8.06)
	vSum = addAngleSpeedVectorYAxisBased(vec1, vec2)
	
	print("speedSum ", vSum[1])
	
	angle, speed = addAngleSpeedVectorXAxisBased(vec1, vec2)
	print("\nX axis based\n")
	print("angle ", math.degrees(angle), " speed ", speed)
