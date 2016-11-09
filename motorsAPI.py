import explorerhat
import time
import timeit
import sys

#text_file = open("OutMotors.txt", "w")

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
	time.sleep(0.03)
        explorerhat.motor.stop()


#Beginning of ET testing
def main():
	direction = sys.argv[1]
	speed = int(sys.argv[2])

	if (direction == "left"):
		turnLeft(speed)
	elif (direction == "right"):
                turnRight(speed)
	elif (direction == "up"):
                accelerate(speed)
	elif (direction == "down"):
              	reverse(speed)
	else:
		print("Wrong code")


if __name__ == "__main__":
	#while True:
	#	start_time = timeit.default_timer()
		main()
#		elapsed = timeit.default_timer() - start_time

#		text_file.write("{}\n".format(elapsed*1000))
		
