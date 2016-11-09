import RM.py
import explorerhat
#from enum import Enum

#Reads the sensor and puts the value at hasDetectedObj
class  SensorTask(TaskType):
    def readSensor():
        hasDetectedObj = explorerhat.input.one.read()

#Reads the input from frontend
class  InputTask(TaskType):
    def readInput():
        inputDirection = sys.read[0]


class  MotorTask(TaskType):
    def turnLeft(speed):
        explorerhat.motor.one.forwards(speed)
        explorerhat.motor.two.backwards(speed)
        stopMotors()

    def turnRight(speed):
        explorerhat.motor.one.backwards(speed)
        explorerhat.motor.two.forwards(speed)
        stopMotors()

    def accelerate(speed):
        explorerhat.motor.one.forwards(speed)
        explorerhat.motor.two.forwards(speed)
        stopMotors()

    def reverse(speed):
        explorerhat.motor.one.backwards(speed)
        explorerhat.motor.two.backwards(speed)
        stopMotors()

    def stopMotors():
        time.sleep(0.2)
        explorerhat.motor.stop()

    dict = {"left": turnLeft, "right": turnRight, "up": accelerate, "down": reverse, "stop": stopMotors}

    def switch(canMoveToDir):
        dict[canMoveToDir]()


#Analyses both results from the sensor and the input
class AnalyserTask(TaskType):
    def analyse():
        if (hasDetectedObj == 0):
            canMoveToDir = inputDirection
        else:
            canMoveToDir = "stop"


#Send to frontend the result of analyser
class ReporterTask(TaskType):
    def report():
        if (hasDetectedObj == 0):
            print "Has detected object!"
        else:
            print "No object ahead!"
