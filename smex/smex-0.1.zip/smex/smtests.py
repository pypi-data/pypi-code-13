from smex import SM
import time
import random

def noRecursionLimit():
	""" 
		When we're using a state machine we can 
		let one function "call" the other, without 
		hitting the recursion limit.
		
		This function will run forever!
	""" 
	def go1():
		SM.go(go2)

	def go2():
		SM.go(go1)

	sm = SM()
	sm.debug(True)
	sm.add(go1)
	sm.add(go2)
	sm.start("go1")


def RecursionLimit():
	def myfunc1():
		myfunc2()

	def myfunc2():
		myfunc1()

	myfunc1()

def simpleMachine():
	""" 

		This is an example of a simple machine 

		A state is a normal function.
		The state has to call 
		SM.go("otherState")
		somewhere
		
	"""
	
	def  scan ():
		# hier mach ich was
		# if True:
		print("\tHello from state scan")
		time.sleep(1)
		if random.randint(0,1):
			print("\tFound targets!")
			SM.go(flying)
		else:
			print ("\tNothing :/")
			SM.go(idle)

	def flying():
		# hier was anders
		print("\tHello from state flying :) ")
		time.sleep(1)
		# raise KeyError ("HALLO")
		SM.go(idle)

	def idle():
		print ("\tIDLEING")
		time.sleep(5)
		SM.go(scan)

	sm = SM() 
	sm.debug(True)
	sm.add(flying) # we add the functions
	sm.add(scan) # to our state
	sm.add(idle) # machine.
	sm.errorState("scan") # when a function is not catching all Exceptions we go to this state
	sm.start("scan") # we start the maschine at the state scan


noRecursionLimit()
# simpleMachine()
