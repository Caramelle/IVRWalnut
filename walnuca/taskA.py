#! /usr/bin/env python
# Core imports
import time
import ev3dev.ev3 as ev3

print ('Welcome to ev3')
def runForward():
    motR.run_direct()
    motL.run_direct()

Tp = 30
motR = ev3.LargeMotor('outA')
motL = ev3.LargeMotor('outD')
colorSensor = ev3.ColorSensor()
btn =ev3.Button()
colorSensor.mode = 'COL-REFLECT'
colorSensor.connected
runForward()


Kp = float(0.3)
Kd = 0.40
Ki = float(0.02)
offset = 55
integral = 0.0
lastError = 0.0
derivative = 0.0
constantCount = 0
state="Time,Turn,Error\n"
lastTurn=1
errors=[]
while not btn.any():
	LightValue = colorSensor.value()
	error = LightValue - offset
	print(error)
	if error == (100-offset):
		constantCount = constantCount + 1
	else:
		constantCount = 0
	if constantCount == 50:
		motR.stop()
		motL.stop()
		break
	integral = 0.5*integral + error
	derivative = error - lastError
	Turn = (Kp*error + Ki*integral + Kd*derivative)*0.8+0.2*lastTurn
	lastTurn=Turn
	powerA=Tp+Turn
    powerC=Tp-Turn
	if powerA>100:
	    powerA=100
        if powerA<-100:
	    powerA=-100
        if powerC>100:
	    powerC=100
        if powerC<-100:
            powerC=-100
 	motR.duty_cycle_sp=powerA
	motL.duty_cycle_sp=powerC
        state=state+str(time.time())+","+str(Turn)+","+str(error)+"\n"
	lastError = error


readings_file = open('oscilationerror.txt', 'w')
readings_file.write(state)
readings_file.close()

ev3.Sound.speak('I\'m done baby').wait()
