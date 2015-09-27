import subprocess
from threading import *
import time
import os
import Astar_GAC

kill_command = "taskkill /F /PID"
kill_command += str(os.getpid())

def changeDelay():
	time.sleep(0.2)
	Astar_GAC.algorithm_delay = delay

print ""
print "-----------------------------"
print "Use GUI? Yes: '1', No: '0'"
use_gui = int( raw_input("") )

if use_gui==1:
	print "Input algorithm delay in milliseconds, blank to use default (0)"
	try:
		delay = (float ( raw_input("")) /1000)
		print delay
	except:
		delay=0
	t = Thread(target=changeDelay)
	t.start()
	import gui
else:
	print "Which graph do you want to solve?"
	graph = int ( raw_input(""))
	Astar_GAC.run(graph)



raw_input("Press any key to stop python processes?")
subprocess.call("taskkill /F /IM python.exe", shell=True)