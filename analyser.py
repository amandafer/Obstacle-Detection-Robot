import motorsAPI
import timeit
import sys

text_file = open("Output.txt", "w")

def analyse(input, speed, sensorReader):
	start_time = timeit.default_timer()

	if (sensorReader == 0):
		print("obstacle") 
	else:
		if (input == "left"):
			motorsAPI.turnLeft(speed)
		elif (input == "right"):
                        motorsAPI.turnRight(speed)
		elif (input == "up"):
                        motorsAPI.accelerate(speed)
		elif (input == "down"):
                       	#motorsAPI.reverse(speed)
			print ("DOWN")

	elapsed = timeit.default_timer() - start_time
	text_file.write("{}\n".format(elapsed*1000))


#Beginning ET test
def main():
	input = sys.argv[1]
	speed = int(sys.argv[2])
	sensorReader = int(sys.argv[3])

	analyse(input, speed, sensorReader)


if __name__ == "__main__":
	while True:
		main()
