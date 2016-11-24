#! /usr/bin/env python
# Core imports
import time
import math
import ev3dev.ev3 as ev3

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
		#print math.fabs(oldVal-g.value())," ", oldVal, " ", g.value()
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
		#print math.fabs(oldVal-g.value())
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


def followLine():
	Kp = float(0.3) 
	Kd =0.4           
	Ki = float(0.02) 
	offset = 55                           # Initialize the variables
	integral = 0.0                          # the place where we will store our integral
	lastError = 0.0                         # the place where we will store the last error value
	derivative = 0.0                        # the place where we will store the derivative
	constantCount = 0
	lastTurn = 1
	while not btn.any():
		LightValue = colorSensor.value()    
		error = LightValue - offset        
		if uS.value() < 50: #if it can detect an object
			motR.stop()
			motL.stop()
			break
		integral = 0.5*integral + error        # calculate the integral
		derivative = error - lastError     # calculate the derivative
		Turn = (Kp*error + Ki*integral + Kd*derivative)*0.8+0.2*lastTurn  # the "P term" the "I term" and the "D term"
		lastTurn=Turn
		powerA=Tp+Turn
		powerC=Tp-Turn
		motR.duty_cycle_sp=powerA
		motL.duty_cycle_sp=powerC
		lastError = error                  #save the current error so it can be the lastError next time around

	time.sleep(0.1)


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

def checkLine():
	global constantWhite
	if checkBlack(colorSensor):
		constantWhite = constantWhite + 1
	else:
		constantWhite = 0
		return 0
	if constantWhite == 10:
		return 1

def runForward():
	motR.duty_cycle_sp = 15
	motL.duty_cycle_sp = 15
	motR.run_direct()
	motL.run_direct()



def moveAway():
	Tp = 30
	Kt = float(0.0235)
	Kp = float(0.22) 
	Kd = float(0.15)        
	Ki = float(0.1)  
	offset = 30                            # Initialize the variables
	integral = 0.0                          # the place where we will store our integral
	lastError = 0.0                         # the place where we will store the last error value
	derivative = 0.0                        # the place where we will store the derivative
	tangent = 0.0
	constantCount = 0
	lastTurn = 0.0
	state="Time,Turn,Error\n"
	while not btn.any():
		DistanceValue = uS.value()    
		error = DistanceValue - offset        
		integral = 0.5*integral + error        
		derivative = error - lastError     
		tangent = error * Kt
		Turn = (Kp*error + Ki*integral + Kd*derivative)*Kt #scale the Turn factor to the tangent
		state=state+str(time.time())+","+str(Turn)+","+str(error)+"\n"
		if checkLine():
			motL.stop()
			motR.stop()	
			break
		print Turn
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

	ev3.Sound.speak('This is the line').wait()
	motL.stop()
	motR.stop()	
        readings_file = open('oscillationturn.txt', 'w')
        readings_file.write(state)
        readings_file.close()


def moveBody():
	oldTime=time.time()
	while(math.fabs(time.time()-oldTime)<1):
		motL.run_direct(duty_cycle_sp=30)
		motR.run_direct(duty_cycle_sp=25)
	motL.stop()
	motR.stop()



def turnEyes():
	oldPos=eyes.position
	while(math.fabs(oldPos-eyes.position)<85):
		eyes.run_direct()
	eyes.stop()


#motors and sensors
motR = ev3.LargeMotor('outA')
motL = ev3.LargeMotor('outD')
uS = ev3.UltrasonicSensor()
uS.mode = 'US-DIST-CM'
colorSensor = ev3.ColorSensor()
eyes = ev3.MediumMotor('outC')
eyes.duty_cycle_sp=70
g = ev3.GyroSensor()
btn =ev3.Button()
colorSensor.mode = 'COL-REFLECT'

# calibration = open('calibration.txt', 'r')
# #global values for calibration
blackMin = 0;
blackMax = 15;
whiteMin = 95;
whiteMax = 100;
constantWhite = 0

Tp = 30
ev3.Sound.speak('Place me on the line').wait()
time.sleep(1)
runForward()
followLine()
ev3.Sound.speak('Found object. Turning left').wait()
turnLeft(g, -2, 100)
turnEyes()
ev3.Sound.speak('moving away from object').wait()
runForward()
moveAway()
motR.stop()
motL.stop()
