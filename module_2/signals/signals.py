#!/usr/bin/python

# working with signals, we need to import it

import signal

# first thing we need to do is to write a signal handler

# it will catch a signal and handler


def ctrlc_handler(signum, frm):
	print 'HAHA, you can not kill me!!'



print "Installing signal handler....."
# signal listener, with the signal listening to as first arg, and handler as second
signal.signal(signal.SIGINT, ctrlc_handler)

print "Donee!!"

while True:
	pass



