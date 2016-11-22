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

	if sensor.value() >= 0 and sensor.value() <=15 :
		return 1
	return 0

def findNextLine(sensor):
	counter = 0
	while True: # checkWhite(colorSensor):
		motR.run_direct(duty_cycle_sp = 25)
		motL.run_direct(duty_cycle_sp = 25)
		sv=sensor.value()
		if sv>=0 and sv<=15:
			counter = counter +1
		if counter == 20:
			break
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


def turnLeft(g,x, dist):
	g.mode='GYRO-ANG'
	oldVal=g.value()
	#print("OLD VALUE: ",oldVal)
	while(math.fabs(oldVal - g.value())< 90 + x):
		#print uS.value()
		print math.fabs(oldVal-g.value())," ", oldVal, " ", g.value()
		motR.run_direct(duty_cycle_sp= -50)
		#print(g.value())
		if btn.any():
			break;
	motR.stop()
	motL.stop()
	    
	    


def turnRight(g, x, dist):
	g.mode='GYRO-ANG'
	oldVal=g.value()
	#print("OLD VALUE: ",oldVal)
	while(math.fabs(oldVal-g.value())<90 + x):
		print math.fabs(oldVal-g.value())
		motL.run_direct(duty_cycle_sp=50)
		if uS.value() <= dist:
			motR.stop()
			motL.stop()
			break
		#print(g.value())
		if btn.any():
			break
	motR.stop()
	motL.stop()

def checkEndLine(error, lastError):
	global constantCount
	if error == 55:
		constantCount = constantCount + 1
	else:
		constantCount = 0
		return 0
	if constantCount == 15:
		#ev3.Sound.speak('I\'m done b').wait()
		return 1

# def followLine():
# 	#ev3.Sound.speak('Following line').wait()
# 	Kp = float(2) # Proportional gain. Start value 1
# 	Kd =0.5           # Derivative gain. Start value 0
# 	Ki = float(0.5) # Integral gain. Start value 0                        # REMEMBER we are using Kd*100 so this is really 100!
# 	offset = 45                           # Initialize the variables
# 	integral = 0.0                          # the place where we will store our integral
# 	lastError = 0.0                         # the place where we will store the last error value
# 	derivative = 0.0                        # the place where we will store the derivative
# 	constantCount = 0
# 	while not btn.any():
# 		LightValue = colorSensor.value()    # what is the current light reading?
# 		if uS.value()<100:
# 			motL.stop()
# 			motR.stop()
# 			break
# 		error = LightValue - offset        # calculate the error by subtracting the offset
# 		# if error == 55:
# 		# 	constantCount = constantCount + 1
# 		# else:
# 		# 	constantCount = 0
# 		# if constantCount == 20:
# 		# 	#ev3.Sound.speak('I\'m done b').wait()
# 		# 	motR.stop()
# 		# 	motL.stop()
# 		# 	break
# 		integral = 0.5*integral + error        # calculate the integral
# 		derivative = error - lastError     # calculate the derivative
# 		Turn = Kp*error + Ki*integral + Kd*derivative  # the "P term" the "I term" and the "D term"
# 		#Turn = Turn/100                      # REMEMBER to undo the affect of the factor of 100 in Kp, Ki and Kd!
# 		# powerA = Tp + Turn                 # the power level for the A motor
# 		# powerC = Tp - Turn                 # the power level for the C motor
# 		(l,r)=steering2(Turn,Tp)
# 		motR.duty_cycle_sp=r
# 		motL.duty_cycle_sp=l
# 		lastError = error                  #save the current error so it can be the lastError next time around
# 		#time.sleep(0.1)
# 	#ev3.Sound.speak('End of loop').wait()
# 	motR.stop()
# 	motL.stop()
# 	time.sleep(0.1)
# 	#return 0

def followLine():
	Kp = float(0.25) # Proportional gain. Start value 1
	Kd = 0.15           # Derivative gain. Start value 0
	Ki = float(0.02) # Integral gain. Start value 0                        # REMEMBER we are using Kd*100 so this is really 
	offset = 45                           # Initialize the variables
	integral = 0.0                          # the place where we will store our integral
	lastError = 0.0                         # the place where we will store the last error value
	derivative = 0.0                        # the place where we will store the derivative
	constantCount = 0
	state="Time,Turn\n"
	while not btn.any():
		LightValue = colorSensor.value()    # what is the current light reading?
		error = LightValue - offset        # calculate the error by subtracting the offset
		# print(error)
		# if error == (100-offset):
		# 	constantCount = constantCount + 1
		# else:
		# 	constantCount = 0
		# if constantCount == 30:
		# 	#ev3.Sound.speak('I\'m done b').wait()
		# 	motR.stop()
		# 	motL.stop()
		# 	break
		if uS.value() < 100:
			motR.stop()
			motL.stop()
			break
		integral = 0.5*integral + error        # calculate the integral
		derivative = error - lastError     # calculate the derivative
		
		Turn = Kp*error + Ki*integral + Kd*derivative  # the "P term" the "I term" and the "D term"
	    #powerA=Tp+Turn
		#Turn = Turn/100                      # REMEMBER to undo the affect of the factor of 100 in Kp, Ki and Kd!
		# powerA = Tp + Turn                 # the power level for the A motor
		# powerC = Tp - Turn                 # the power level for the C motor
	    #powerA=Tp+Turn
		powerA=Tp+Turn
		powerC=Tp-Turn
		if powerA > 100:
			powerA = 100
		if powerC > 100:
			powerC = 100
		if powerA < -100:
			powerA = -100
		if powerC < -100:
			powerC = -100
	 	motR.duty_cycle_sp=powerA
		motL.duty_cycle_sp=powerC
		state=state+str(time.time())+","+str(Turn)+"\n"
		lastError = error                  #save the current error so it can be the lastError next time around
		#time.sleep(0.1)

def findObj(dist):
	runForward()
	while True:
		motR.duty_cycle_sp = 30
		motL.duty_cycle_sp = 30
		print uS.value()
		if uS.value() <= dist:
			motL.stop()
			motR.stop()
			break
	motR.stop()
	motL.stop()

def runForward():
    motR.run_direct()
    motL.run_direct()

def moveAway():
	Tp = 30
	ev3.Sound.speak('moving away from object').wait()
	Kp = float(0.22) # Proportional gain. Start value 1
	Kd = 0.15           # Derivative gain. Start value 0
	Ki = float(0.02) # Integral gain. Start value 0                        # REMEMBER we are using Kd*100 so this is really 
	offset = 100                            # Initialize the variables
	integral = 0.0                          # the place where we will store our integral
	lastError = 0.0                         # the place where we will store the last error value
	derivative = 0.0                        # the place where we will store the derivative
	constantCount = 0
	state="Time,Turn\n"
	while not btn.any():
		DistanceValue = uS.value()    # what is the current light reading?
		error = DistanceValue - offset        # calculate the error by subtracting the offset
		print(error)
		# if error == (100-offset):
		# 	constantCount = constantCount + 1
		# else:
		# 	constantCount = 0
		# if constantCount == 30:
		# 	#ev3.Sound.speak('I\'m done b').wait()
		# 	motR.stop()
		# 	motL.stop()
		# 	break
		integral = 0.5*integral + error        # calculate the integral
		derivative = error - lastError     # calculate the derivative
		Turn = Kp*error + Ki*integral + Kd*derivative  # the "P term" the "I term" and the "D term"
	    #powerA=Tp+Turn
		#Turn = Turn/100                      # REMEMBER to undo the affect of the factor of 100 in Kp, Ki and Kd!
		# powerA = Tp + Turn                 # the power level for the A motor
		# powerC = Tp - Turn                 # the power level for the C motor
	    #powerA=Tp+Turn
		powerA=Tp+Turn
		powerC=Tp-Turn
		if powerA > 100:
			powerA = 100
		if powerC > 100:
			powerC = 100
		if powerA < -100:
			powerA = -100
		if powerC < -100:
			powerC = -100
		if uS.value() > 500:
			motR.stop()
			motL.stop()
			break
		motR.duty_cycle_sp=powerA
		motL.duty_cycle_sp=powerC
		state=state+str(time.time())+","+str(Turn)+"\n"
		lastError = error                  #save the current error so it can be the lastError next time around
	#time.sleep(0.1)
	# while uS.value()<200:
	# 	motR.run_direct()
	# 	motL.run_direct()
	motL.stop()
	motR.stop()	

def moveBody():
	oldTime=time.time()
	while(math.fabs(time.time()-oldTime)<1):
		motL.run_direct(duty_cycle_sp=30)
		motR.run_direct(duty_cycle_sp=25)
	motL.stop()
	motR.stop()



def turnEyes():
	oldPos=eyes.position
	while(math.fabs(oldPos-eyes.position)<80):
		eyes.run_direct()
	eyes.stop()


# def steering2(course, power):
# 	"""
# 	Computes how fast each motor in a pair should turn to achieve the
# 	specified steering.
# 	Input:
# 		course [-100, 100]:
# 		* -100 means turn left as fast as possible,
# 		*  0   means drive in a straight line, and
# 		*  100  means turn right as fast as possible.
# 		* If >100 power_right = -power
# 		* If <100 power_left = power
# 	power: the power that should be applied to the outmost motor (the one
# 		rotating faster). The power of the other motor will be computed
# 		automatically.
# 	Output:
# 		a tuple of power values for a pair of motors.
# 	Example:
# 		for (motor, power) in zip((left_motor, right_motor), steering(50, 90)):
# 			motor.run_forever(speed_sp=power)
# 	"""
# 	if course >= 0:
# 		if course > 100:
# 			power_right = 0
# 			power_left = power
# 		else:
# 			power_left = power
# 			power_right = power - ((power * course) / 100)
# 	else:
# 		if course < -100:
# 			power_left = 0
# 			power_right = power
# 		else:
# 			power_right = power
# 			power_left = power + ((power * course) / 100)
# 	return (int(power_left), int(power_right))

#motors and sensors
motR = ev3.LargeMotor('outA')
motL = ev3.LargeMotor('outD')
uS = ev3.UltrasonicSensor()
uS.mode = 'US-DIST-CM'
colorSensor = ev3.ColorSensor()
eyes = ev3.MediumMotor('outC')
eyes.duty_cycle_sp=60
g = ev3.GyroSensor()
btn =ev3.Button()
colorSensor.mode = 'COL-REFLECT'

# calibration = open('calibration.txt', 'r')
# #global values for calibration
blackMin = 0;
blackMax = 15;
whiteMin = 95;
whiteMax = 100;

Tp = 30
ev3.Sound.speak('Place me on the line').wait()
time.sleep(1)
runForward()
followLine()
ev3.Sound.speak('Found object. Turning left').wait()
turnLeft(g, -2, 100)
turnEyes()
runForward()
moveAway()
# ev3.Sound.speak('moving my body').wait()
# moveBody()
ev3.Sound.speak('turning right').wait()
turnRight(g,10, 200)
runForward()
# #ev3.Sound.speak('lookin for object').wait()
# #findObj(200)
# #ev3.Sound.speak('found object').wait()
# moveBody()
# ev3.Sound.speak('moving away from object').wait()
moveAway()
# ev3.Sound.speak('moving my body').wait()
# moveBody()
# ev3.Sound.speak('turrning right').wait()
# turnRight(g, 0, 100)
# runForward()
# findNextLine(colorSensor)
# followLine()

