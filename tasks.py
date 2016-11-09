import RM.py
import explorerhat
#from enum import Enum

#A task instance
class TaskIns(object):
     #Constructor (should only be invoked with keyword parameters)
    def __init__(self, start, end, priority, name):
        self.start    = start
        self.end      = end
        self.usage    = 0
        self.priority = priority
        self.name     = name.replace("\n", "")
        self.id = int(random.random() * 10000)

    #Allow an instance to use the cpu (periodic)
    def use(self, usage):
        self.usage += usage
        if self.usage >= self.end - self.start:
            return True
        return False

    #Default representation
    def __repr__(self):
        return str(self.name) + "#" + str(self.id) + " - start: " + str(self.start) + " priority: " + str(self.priority) + budget_text

    #Get name as Name#id
    def get_unique_name(self):
        return str(self.name) + "#" + str(self.id)


#Task types (templates for periodic tasks)
class TaskType(object):
    #Constructor
    def __init__(self, period, release, execution, deadline, name):
        self.period    = period
        self.release   = release
        self.execution = execution
        self.deadline  = deadline
        self.name      = name

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
