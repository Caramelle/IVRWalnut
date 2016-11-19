#! /usr/bin/env python
# Core imports
import time
import math
import ev3dev.ev3 as ev3

# Local Imports
import tutorial as tutorial
import utilities
import openLoopControl as olc

print ('Welcome to ev3')

def checkWhite(sensor):
	if sensor.value() >= whiteMin and sensor.value() <= whiteMax:
		return 1 
	return 0

def checkBlack(sensor):
	if sensor.value() >= blackMin and sensor.value() >= blackMax:
		return 1
	return 0

def findNextLine():
	while checkWhite(colorSensor):
		motR.run_direct(duty_cycle_sp = 25)
		motL.run_direct(duty_cycle_sp = 25)
	motR.stop()
	motL.stop()
	ev3.Sound.speak('Found start of line').wait()

def findEndLine():
	while checkBlack(colorSensor):
		motR.run_direct(duty_cycle_sp = 18)
		motL.run_direct(duty_cycle_sp = 18)
	motR.stop()
	motL.stop()
	ev3.Sound.speak('Found end of line').wait()


def turnLeft(g):
	g.mode='GYRO-ANG'
	oldVal=g.value()
	print("OLD VALUE: ",oldVal)
	while(math.fabs(oldVal-g.value())<60):
	    motL.run_direct(duty_cycle_sp=40)
	    print(g.value())
	    if btn.any():
	        break;


def turnRight(g):
	g.mode='GYRO-ANG'
	oldVal=g.value()
	print("OLD VALUE: ",oldVal)
	while(math.fabs(oldVal-g.value())<80):
	    motR.run_direct(duty_cycle_sp=40)
	    print(g.value())
	    if btn.any():
	        break;

def checkEndLine(error, lastError):
	global constantCount
	if error == 55:
		constantCount = constantCount + 1
	else:
		constantCount = 0
		return 0
	if constantCount == 25:
		#ev3.Sound.speak('I\'m done b').wait()
		return 1

def followLine():
	ev3.Sound.speak('Following line').wait()
	Kp = float(2) # Proportional gain. Start value 1
	Kd =0.5           # Derivative gain. Start value 0
	Ki = float(0.5) # Integral gain. Start value 0                        # REMEMBER we are using Kd*100 so this is really 100!
	offset = 45                           # Initialize the variables
	integral = 0.0                          # the place where we will store our integral
	lastError = 0.0                         # the place where we will store the last error value
	derivative = 0.0                        # the place where we will store the derivative
	constantCount = 0
	while not btn.any():
		LightValue = colorSensor.value()    # what is the current light reading?
		error = LightValue - offset        # calculate the error by subtracting the offset
		if error == lastError:
			constantCount = constantCount + 1
		else:
			constantCount = 0
		if constantCount == 20:
			#ev3.Sound.speak('I\'m done b').wait()
			motR.stop()
			motL.stop()
			break
		integral = 0.5*integral + error        # calculate the integral
		derivative = error - lastError     # calculate the derivative
		Turn = Kp*error + Ki*integral + Kd*derivative  # the "P term" the "I term" and the "D term"
		#Turn = Turn/100                      # REMEMBER to undo the affect of the factor of 100 in Kp, Ki and Kd!
		# powerA = Tp + Turn                 # the power level for the A motor
		# powerC = Tp - Turn                 # the power level for the C motor
		(l,r)=steering2(Turn,Tp)
		motR.duty_cycle_sp=r
		motL.duty_cycle_sp=l
		lastError = error                  #save the current error so it can be the lastError next time around
		#time.sleep(0.1)
	#ev3.Sound.speak('End of loop').wait()
	time.sleep(0.1)
	#return 0

def runForward():
    motR.run_direct()
    motL.run_direct()


def steering2(course, power):
	"""
	Computes how fast each motor in a pair should turn to achieve the
	specified steering.
	Input:
		course [-100, 100]:
		* -100 means turn left as fast as possible,
		*  0   means drive in a straight line, and
		*  100  means turn right as fast as possible.
		* If >100 power_right = -power
		* If <100 power_left = power
	power: the power that should be applied to the outmost motor (the one
		rotating faster). The power of the other motor will be computed
		automatically.
	Output:
		a tuple of power values for a pair of motors.
	Example:
		for (motor, power) in zip((left_motor, right_motor), steering(50, 90)):
			motor.run_forever(speed_sp=power)
	"""
	if course >= 0:
		if course > 100:
			power_right = 0
			power_left = power
		else:
			power_left = power
			power_right = power - ((power * course) / 100)
	else:
		if course < -100:
			power_left = 0
			power_right = power
		else:
			power_right = power
			power_left = power + ((power * course) / 100)
	return (int(power_left), int(power_right))

#motors and sensors
motR = ev3.LargeMotor('outA')
motL = ev3.LargeMotor('outD')
colorSensor = ev3.ColorSensor()
g = ev3.GyroSensor()
btn =ev3.Button()
colorSensor.mode = 'COL-REFLECT'

# calibration = open('calibration.txt', 'r')
# #global values for calibration
blackMin = 10;
blackMax = 30;
whiteMin = 95;
whiteMax = 100;

Tp = 50
ev3.Sound.speak('Place me on the line').wait()
time.sleep(1)
runForward()
followLine()
ev3.Sound.speak('Looking for line on the left').wait()
turnLeft(g)
findNextLine()
#findEndLine()
# motR.stop()
# motL.stop()
ev3.Sound.speak('Turning around to follow line').wait()
turnRight(g)
motR.stop()
motL.stop()
runForward()
followLine()
# turnRight(g)
# ev3.Sound.speak('Looking for line on the right').wait()
# findNextLine()
# turnLeft(g)
# ev3.Sound.speak('Turning around to follow line').wait()
# followLine()
motR.stop()
motL.stop()
# findEndLine()
# motL.stop()
# turnRight()
# ev3.Sound.speak('Found love').wait()
# followLine()
# ev3.Sound.speak('Followed love').wait()
# time.sleep(0.1)
# while not btn.any():
# 	gyroSensor.mode ='GYRO-ANG'
# 	print gyroSensor.value()
# 	#ev3.Sound.speak('turning around').wait()
# 	motL.duty_cycle_sp=50
# 	motR.duty_cycle_sp=-50

# motL.run_forever()
# motR.run_forever()
# turnRight()
