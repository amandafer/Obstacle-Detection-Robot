import explorerhat
import time

def turnLeft(speed) {
	explorerhat.motor.one.backwards(speed)
	explorerhat.motor.two.forwards(speed)
	sleep.time(0.5)
	explorerhat.motor.stop()
}

def turnRight(speed) {
	explorerhat.motor.one.forwards(speed)
	explorerhat.motor.two.backwards(speed)
	sleep.time(0.5)
	explorerhat.motor.stop()
}

def accelerate(speed) {
	explorerhat.motor.one.forwards(speed)
	explorerhat.motor.two.forwards(speed)
	sleep.time(0.5)
	explorerhat.motor.stop()
}

def reverse(speed) {
	explorerhat.motor.one.backwards(speed)
        explorerhat.motor.two.backwards(speed)
        sleep.time(0.5)
        explorerhat.motor.stop()
}
