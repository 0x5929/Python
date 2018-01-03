#!/usr/bin/python

# import the subprocess module
import subprocess

# a subprocess helps invoke another process, so you can interact with it
# example, of a ps process

# to execute a subprocess, you can just use the call method
# passing in a list with first value is the process name 
# second value is the arg for the process

subprocess.call(['ps', 'aux'])

subprocess.call(['ls', '-al'])


## now what if we want to use all the above output in our application

## we can use subprocess.check_output instead of call

## and we can put the result into a variable like such


#lines = subprocess.call(['ls'])

#print lines

# another way to use subprocess is to map the stdin stdout and stderr 
# for us to interact with it

# example: below needs to be inputted in the python shell, 
# will not work here, b/c the stdout of this file is mapped to subprocess.PIPE
# and i do not how to retrieve it back to the terminal yet.  

#handle = subprocess.Popen("ls", stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)

#handle.stdout.read()

