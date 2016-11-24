#! /usr/bin/env python
# Core imports
import time
import math
import ev3dev.ev3 as ev3


class walnut:
    def __init__(self):
        self.motR = ev3.LargeMotor('outA')
        self.motL = ev3.LargeMotor('outD')
        self.colorSensor = ev3.ColorSensor()
        self.g = ev3.GyroSensor()
        self.btn =ev3.Button()
        self.colorSensor.mode = 'COL-REFLECT'
        self.g.mode='GYRO-ANG'
        self.Tp=30
        self.startAngle=self.g.value()
        self.endAngle=self.g.value()




    def getDisplacement(self):
        return self.endAngle-self.startAngle
    def findNextLine(self):
        self.startAngle=self.g.value()
    	counter = 0
    	while True: # checkWhite(colorSensor):
    		self.motR.run_direct(duty_cycle_sp = 25)
    		self.motL.run_direct(duty_cycle_sp = 25)
    		sv=self.colorSensor.value()
    		if sv>=0 and sv<=15:
    			counter = counter +1
    		if counter == 20:
    			break
    	self.motR.stop()
    	self.motL.stop()
    	ev3.Sound.speak('Found start of line').wait()
        self.endAngle=self.g.value()


    def checkLine(self):
    	colour = self.colorSensor.value()
    	if colour > 0 and colour <15:
    		constantWhite = constantWhite + 1
    	else:
    		constantWhite = 0
    		return 0
    	if constantWhite == 5:
    		#ev3.Sound.speak('I\'m done b').wait()
    		return 1


    def turnLeft(self,x):
        self.startAngle=self.g.value()
    	self.g.mode='GYRO-ANG'
    	oldVal=self.g.value()
    	while(math.fabs(oldVal-self.g.value())<88 + x):
    	    self.motL.run_direct(duty_cycle_sp=40)
    	    if self.btn.any():
    	        break;
    	self.motR.stop()
    	self.motL.stop()
        self.endAngle=self.g.value()




    def turnRight(self,x):
        self.startAngle=self.g.value()
    	self.g.mode='GYRO-ANG'
    	oldVal=self.g.value()
    	while(math.fabs(oldVal-self.g.value())<88 + x):
    	    self.motR.run_direct(duty_cycle_sp=40)
    	    if self.btn.any():
    	        break;
    	self.motR.stop()
    	self.motL.stop()
        self.endAngle=self.g.value()



    def followLine(self):
    	#ev3.Sound.speak('Following line').wait()
        self.startAngle=self.g.value()
    	Kp = float(0.3)
    	Kd =0.4
    	Ki = float(0.02)
    	offset = 55
    	integral = 0.0
    	lastError = 0.0
    	derivative = 0.0
    	constantCount = 0
    	lastTurn = 1
    	while not self.btn.any():
    		LightValue = self.colorSensor.value()
    		error = LightValue - offset        
    		if error == 100-offset:
    			constantCount = constantCount + 1
    		else:
    			constantCount = 0
    		if constantCount == 20:
    			self.motR.stop()
    			self.motL.stop()
    			break
    		integral = 0.5*integral + error
    		derivative = error - lastError
    		Turn = (Kp*error + Ki*integral + Kd*derivative)*0.8+0.2*lastTurn
    		lastTurn=Turn
    		powerA=self.Tp+Turn
    		powerC=self.Tp-Turn

    		self.motR.duty_cycle_sp=powerA
    		self.motL.duty_cycle_sp=powerC
    		lastError = error
    	self.endAngle=self.g.value()
        ev3.Sound.speak('Finished line').wait()


    def runForward(self):
        self.motR.run_direct()
        self.motL.run_direct()



    def brokenLines(self):
        ev3.Sound.speak('Place me on the line').wait()
        self.runForward()

        #line 1
        self.followLine()

        self.turnLeft(self.getDisplacement())


        self.findNextLine()


        self.turnRight(-self.getDisplacement())
        self.startAngle=self.g.value()

       #line 2
        self.runForward()
        self.followLine()


        self.turnRight(-self.getDisplacement())

        self.findNextLine()
        self.turnLeft(self.getDisplacement())
        #line 3
        self.runForward()
        self.followLine()

        self.turnRight(-self.getDisplacement())
        self.findNextLine()
        self.turnLeft(self.getDisplacement())
        #line 4
        self.runForward()
        self.followLine()

        self.motL.stop()
        self.motR.stop()


wally=walnut()
wally.brokenLines()
