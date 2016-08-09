"""
	Smex is a simple state machine.
	Usage:

		from smex import SM
		
		def go1():
			SM.go(go2)

		def go2():
			SM.go(go1)

		sm = SM()
		sm.add(go1)
		sm.add(go2)
		sm.start("go1")

	Get more help/examples by looking at the source code of
	smex.py , pissbot.py , smtests.py

"""

from .smex import SM