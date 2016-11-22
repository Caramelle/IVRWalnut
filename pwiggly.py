#! /usr/bin/env python
# Core imports
import time
import ev3dev.ev3 as ev3
#import matplotlib as plt

# Local Imports
import tutorial as tutorial
import utilities
import openLoopControl as olc

print ('Welcome to ev3')
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
			power_right = power - course
	else:
		if course < -100:
			power_left = 0
			power_right = power
		else:
			power_right = power
			power_left = power + course
	return (int(power_left), int(power_right))

Tp = 30
motR = ev3.LargeMotor('outA')
motL = ev3.LargeMotor('outD')
colorSensor = ev3.ColorSensor()
btn =ev3.Button()
colorSensor.mode = 'COL-REFLECT'
colorSensor.connected
runForward()
# 0.25 0.15 works okeish
Kp = float(0.25) # Proportional gain. Start value 1
Kd = 0.15         # Derivative gain. Start value 0
Ki = float(0.02) # Integral gain. Start value 0                        # REMEMBER we are using Kd*100 so this i

Kp = float(0.25) # Proportional gain. Start value 1
Kd = 0.15         # Derivative gain. Start value 0
Ki = float(0.02) # Integral gain. Start value 0    really  
offset = 55                           # Initialize the variables
integral = 0.0                          # the place where we will store our integral
lastError = 0.0                         # the place where we will store the last error value
derivative = 0.0                        # the place where we will store the derivative
constantCount = 0
state="Time,Turn\n"
lastTurn=1
while not btn.any():
	LightValue = colorSensor.value()    # what is the current light reading?
	error = LightValue - offset        # calculate the error by subtracting the offset
	print(error)
	if error == (100-offset):
		constantCount = constantCount + 1
	else:
		constantCount = 0
	if constantCount == 1550:
		#ev3.Sound.speak('I\'m done b').wait()
		motR.stop()
		motL.stop()
		break
	integral = 0.5*integral + error        # calculate the integral
	derivative = error - lastError     # calculate the derivative
	
	Turn = (Kp*error + Ki*integral + Kd*derivative)*1+0.0*lastTurn  # the "P term" the "I term" and the "D term"
        lastTurn=Turn
    #powerA=Tp+Turn
	#Turn = Turn/100                      # REMEMBER to undo the affect of the factor of 100 in Kp, Ki and Kd!
	# powerA = Tp + Turn                 # the power level for the A motor
	# powerC = Tp - Turn                 # the power level for the C motor
    #powerA=Tp+Turn
	powerA=Tp+Turn
        powerC=Tp-Turn
	if powerA>100:
	    powerA=100
        if powerA<-100:
	    powerA=-100    
 	motR.duty_cycle_sp=powerA
	motL.duty_cycle_sp=powerC
        #state=state+str(time.time())+","+str(Turn)+"\n"
	lastError = error                  #save the current error so it can be the lastError next time around
	#time.sleep(0.1)

#readings_file = open('oscilationKp4.txt', 'w')
#readings_file.write(state)
#readings_file.close()
ev3.Sound.speak('I\'m done baby').wait()
