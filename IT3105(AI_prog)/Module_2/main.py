import subprocess

print ""
print "-------------------------------"
print "Use GUI? Yes: '1', No: '0'"
use_gui = int( raw_input("") )

if use_gui==1:
	print "Input algorithm delay in seconds, blank to use default(0)"
	try:
		delay = float ( raw_input(""))
	except:
		delay=0
	import gui
	raw_input("Press any key to stop python processes?")
	# import Astar_GAC
else:
	print "Which graph do you want to solve?"
	graph = int ( raw_input(""))
	import Astar_GAC
	Astar_GAC.run(graph)
	raw_input("Quit?")
subprocess.call("taskkill /F /IM python.exe", shell=True)