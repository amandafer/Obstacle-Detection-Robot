import string
import random
import fractions
import tasks.py

#Global variables
hasDetectedObj = 0
inputDirection = "up"
canMoveToDir = inputDirection
speed = 60

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
    html_color = { 'Task1':'white', 'Task2':'white', 'Task3':'white', 'Task4':'white', 'Task5':'white', 'Empty':'grey', 'Finish':'black'}
    #taskfile = open('tasks.txt')
    #lines = taskfile.readlines()
    sensor = SensorTask(30, 0, 10, 30, "sensor")
    input_ = InputTask(40, 0, 10, 40, "input_")
    analyser = AnalyserTask(40, 0, 8, 30, "analyser")
    motor = MotorTask(60, 0, 4, 60, "motor")
    reporter = ReporterTask(120, 0, 6, 120, "reporter")

    task_types = [sensor, input_, analyser, motor, reporter]
    tasks = []
    hyperperiod = []

    #Allocate task types
    #for line in lines:
    #    line = line.split(' ')
    #    for i in range (0,4):
    #        line[i] = int(line[i])
    #    if len(line) == 5:
    #        name = line[4]
    #    elif len(line) == 4:
    #        name = 'Task'
    #    else:
    #        raise Exception('Invalid tasks.txt file structure')
    #    if int(line[0])>0:
    #        task_types.append(TaskType(period=line[0], release=line[1], execution=line[2], deadline=line[3], name=name))

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

    #Html output start
    html = "<!DOCTYPE html><html><head><title>RM Scheduling</title></head><body>"

    #Check utilization
    utilization = 0
    for task_type in task_types:
        utilization += float(task_type.execution) / float(task_type.period)
    if utilization > 1:
        print 'Utilization error!'
        html += '<br /><br />Utilization error!<br /><br />'

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
            html += '<div style="float: left; text-align: center; width: 110px; height: 20px; background-color:' + html_color[on_cpu.name] + ';">' + on_cpu.get_unique_name() + '</div>'
            if on_cpu.use(clock_step):
                tasks.remove(on_cpu)
                html += '<div style="float: left; text-align: center; width: 10px; height: 20px; background-color:' + html_color['Finish'] + ';"></div>'
                print "Finish!" ,
        else:
            print 'No task uses the processor. '
            html += '<div style="float: left; text-align: center; width: 110px; height: 20px; background-color:' + html_color['Empty'] + ';">Empty</div>'
        print "\n"

    #Print remaining periodic tasks
    html += "<br /><br />"
    for p in tasks:
        print p.get_unique_name() + " is dropped due to overload!"
        html += "<p>" + p.get_unique_name() + " is dropped due to overload!</p>"

    #Html output end
    html += "</body></html>"
    output = open('output.html', 'w')
    output.write(html)
    output.close()
