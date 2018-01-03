#!/usr/bin/python



## importing os module
import os



# examples of spawning new processes with os.exec* family of cmds

## invoking a new process using execvp
# first arg is the file/process name  you want to invoke.
# next arg is a list of args you want to pass to invoke that  process
# typically the first key should always be the process it self, as if you were running it on the terminal
# so if i want to start the ping process, to ping google.com
# please see example below: 

# remember execvp will overlay the current process, meaning it will stop  the python program to run
# the program specified

os.execvp("ping", ["ping", "www.google.com"])




