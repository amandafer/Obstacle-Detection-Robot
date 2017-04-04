import explorerhat
import random
import time
import socket

def initializeSock():
    global sock, addr, inputDirection, speed
	
    speed = 100
    inputDirection = "stop"

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("", 5005))

    sock.settimeout(0.01)

    addr = ""

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
        return str(self.name)

    #Get name as Name#id
    def get_unique_name(self):
        return str(self.name)


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
    def task(self):
        global hasDetectedObj 
	hasDetectedObj = explorerhat.input.one.read()

#Reads the input from frontend
class  InputTask(TaskType):
    def task(self):
        global inputDirection 
	inputDirection = "stop"
	global speed
        global addr
	
        try:
            msg, addr = sock.recvfrom(100)
            
            split = msg.split()

            inputDirection = split[0]
            speed = int(split[1])

        except socket.timeout:
            pass

class  MotorTask(TaskType):
    def turnLeft(self):
        explorerhat.motor.one.forwards(speed)
        explorerhat.motor.two.backwards(speed)

    def turnRight(self):
        explorerhat.motor.one.backwards(speed)
        explorerhat.motor.two.forwards(speed)

    def accelerate(self):
        explorerhat.motor.one.forwards(speed)
        explorerhat.motor.two.forwards(speed)

    def reverse(self):
        explorerhat.motor.one.backwards(speed)
        explorerhat.motor.two.backwards(speed)

    def stopMotors(self):
        time.sleep(0.2)
        explorerhat.motor.stop()


    def task(self):
	dict_ = {"left":self.turnLeft, "right":self.turnRight, "up":self.accelerate, "down":self.reverse, "stop":self.stopMotors}

        dict_[canMoveToDir]()


#Analyses both results from the sensor and the input
class AnalyserTask(TaskType):
    def task(self):
        if (hasDetectedObj == 1):
            global canMoveToDir 
	    canMoveToDir = inputDirection
        else:
            if (inputDirection == "up"):
                canMoveToDir = "stop"
            else:
                canMoveToDir = inputDirection


#Send to frontend the result of analyser
class ReporterTask(TaskType):
    def task(self):
	if (addr == ""):
            return

	print ("address: ", addr)

        if (hasDetectedObj == 0):
            sock.sendto("Obstacle Detected!", (addr[0], 5005))
	else:
	    sock.sendto("", (addr[0], 5005))
