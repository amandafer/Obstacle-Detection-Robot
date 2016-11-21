import string
import random
import fractions
from tasks import *

#Global variables
hasDetectedObj = 0
inputDirection = "up"
canMoveToDir = inputDirection
speed = 100

def _lcm(a,b): return abs(a * b) / fractions.gcd(a,b) if a and b else 0

def lcm(a):
    return reduce(_lcm, a)


#Priority comparison
def priority_cmp(one, other):
    if one.priority < other.priority:
        return -1
    elif one.priority > other.priority:
        return 1
    return 0


#Rate monotonic comparison
def tasktype_cmp(self, other):
    if self.period < other.period:
        return -1
    if self.period > other.period:
        return 1
    return 0


if __name__ == '__main__':
    #Variables
    sensor = SensorTask(6, 0, 1, 6, "sensor")
    input_ = InputTask(8, 0, 2, 8, "input_")
    analyser = AnalyserTask(8, 0, 1, 8, "analyser")
    motor = MotorTask(12, 0, 2, 12, "motor")
    reporter = ReporterTask(24, 0, 1, 24, "reporter")

    task_types = [sensor, input_, analyser, motor, reporter]
    tasks = []
    hyperperiod = []


    #Calculate hyperperiod
    for task_type in task_types:
        hyperperiod.append(task_type.period)
    hyperperiod = lcm(hyperperiod)

    #Sort types rate monotonic
    task_types = sorted(task_types, tasktype_cmp)


    #Create task instances
    for i in xrange(0, hyperperiod):
        for task_type in task_types:
            if  (i - task_type.release) % task_type.period == 0 and i >= task_type.release:
                start = i
                end = start + task_type.execution
                priority = task_type.period
                tasks.append(TaskIns(start=start, end=end, priority=priority, name=task_type.name))


    #Check utilization
    utilization = 0
    for task_type in task_types:
        utilization += float(task_type.execution) / float(task_type.period)
    if utilization > 1:
        print 'Utilization error!'


    #Simulate clock
    clock_step = 1
    for i in xrange(0, hyperperiod, clock_step):
        #Fetch possible tasks that can use cpu and sort by priority
        possible = []
        for t in tasks:
            if t.start <= i:
                possible.append(t)
        possible = sorted(possible, priority_cmp)

        #Select task with highest priority
        if len(possible) > 0:
            on_cpu = possible[0]
            print on_cpu.get_unique_name() , " uses the processor. " ,
            for task in task_types:
		task_name = on_cpu.get_unique_name();
		if task.name in task_name:
		   task.task()

	    if on_cpu.use(clock_step):
                tasks.remove(on_cpu)
                print "Finish!" ,
        	#raw_input()
	else:
            print 'No task uses the processor. '
        print "\n"

    #Print remaining periodic tasks
    for p in tasks:
        print p.get_unique_name() + " is dropped due to overload!"

