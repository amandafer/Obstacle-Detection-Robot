import signal
import collections
import itertools
import string
import random
import fractions
from tasks import *

#Define timeout exception handler
def handler(signum, frame):
    print "Execution timed out!"
    #raise Exception()

def _lcm(a,b): return abs(a * b) / fractions.gcd(a,b) if a and b else 0

def lcm(a):
    return reduce(_lcm, a)

#Advances iterator n positions
def consume(iterator, n):
    collections.deque(itertools.islice(iterator, n-1))#master hacking

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
    sensor = SensorTask(6, 0, 1.0, 6, "sensor")
    input_ = InputTask(8, 0, 2.0, 8, "input_")
    analyser = AnalyserTask(8, 0, 1.0, 8, "analyser")
    motor = MotorTask(12, 0, 4.0, 12, "motor")
    reporter = ReporterTask(24, 0, 1.0, 24, "reporter")

    task_types = [sensor, input_, analyser, motor, reporter]
    tasks = []
    hyperperiod = []

    initializeSock()

    #Calculate hyperperiod
    for task_type in task_types:
        hyperperiod.append(task_type.period)
    hyperperiod = lcm(hyperperiod)

    #Sort types rate monotonic
    task_types = sorted(task_types, tasktype_cmp)

    while True:
     #Create task instances
     iterator = range(0, hyperperiod).__iter__()
     for i in iterator:
         for task_type in task_types:
             if  (i - task_type.release) % task_type.period == 0 and i >= task_type.release:
                 start = i
                 end = start + task_type.execution
                 priority = task_type.period
                 tasks.append(TaskIns(start=start, end=end, priority=priority, name=task_type.name))
                 consume(iterator, int(task_type.execution))

     #Check util ization
     utilization = 0
     for task_type in task_types:
         utilization += float(task_type.execution) / float(task_type.period)
     if utilization > 1:
         print 'Utilization error!'


     #Simulate clock
     clock_step = 1
     hyper_iter = range(0, hyperperiod).__iter__()
     for i in hyper_iter:
         #Fetch possible tasks that can use cpu and sort by priority
         possible = []
         for t in tasks:
             if t.start <= i:
                 possible.append(t)
         possible = sorted(possible, priority_cmp)

         #Select task with highest priority
         if len(possible) > 0:
             on_cpu = possible[0]
             #print on_cpu.get_unique_name() , " uses the processor. " ,
             for task in task_types:
                 task_name = on_cpu.get_unique_name();
                 if task.name in task_name:
                     try:
                         timer = task.execution/100
                         print "task: %s -- timer %.3f" % (task.name, timer)
                         signal.signal(signal.SIGALRM, handler)
                         signal.setitimer(signal.ITIMER_REAL, timer)
                         task.task()
                         #print "clock: ", i
                         #print "task exec: ", task.execution
                     except Exception, e:
                         pass
                     finally:
                         ftimer = signal.getitimer(signal.ITIMER_REAL)
                         print "final timer: %.3f" % ftimer[0]
                         signal.setitimer(signal.ITIMER_REAL, 0)
                         consume(hyper_iter, int(task.execution))

             tasks.remove(on_cpu)
             #print "Finish!" ,
             #raw_input()
         else:
             #print 'No task uses the processor. '
	     pass

     #Print remaining periodic tasks
     for p in tasks:
         print p.get_unique_name() + " is dropped due to overload!"
