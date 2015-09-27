import subprocess
from threading import *
import time
import Astar_GAC


def changeDelay():
	time.sleep(2)
	Astar_GAC.algorithm_delay = delay

print ""
print "-------------------------------"
print "Use GUI? Yes: '1', No: '0'"
use_gui = int( raw_input("") )

if use_gui==1:
	print "Input algorithm delay in seconds, blank to use default (0)"
	try:
		delay = float ( raw_input(""))
	except:
		delay=0
	t = Thread(target=changeDelay)
	t.start()
	import gui
	raw_input("Press any key to stop python processes?")
	# import Astar_GAC
else:
	print "Which graph do you want to solve?"
	graph = int ( raw_input(""))
	Astar_GAC.run(graph)
	raw_input("Quit?")



subprocess.call("taskkill /F /IM python.exe", shell=True)