import explorerhat
import timeit

text_file = open("Output.txt", "w")

#Read the output from the sensor. Out must be connected to input1
while True:
	start_time = timeit.default_timer()

	hasDetectedObj = explorerhat.input.one.read()


	if (hasDetectedObj == 0):
		print "Detected object"

	elapsed = timeit.default_timer() - start_time

	text_file.write("{}\n".format(elapsed*1000))
