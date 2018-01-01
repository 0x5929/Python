#!/usr/bin/python


## initializing age

age = 24 

## while loop will continue until test statement is invalid 

while age > 10: 
	
	## input from user
	## converting string age to int age: 

	age = int(raw_input("what is your age? "))

	if age >= 21:
		print "Your age is > 21, and you can drink legally!!"
		break  
	elif age < 21 and age >= 18:
		print "You are an adult but you cant drink"
		continue
	elif age < 18 and age >= 14:
		print "Enjoy High school"
		pass
	elif age < 14:
		print "Enjoy Jr High"
		continue  
	else: 
		print "Your age is <= 10"
		pass
else:
	print "ENJOY ELEMENTARY SCHOOL!"
## pass does nothing, it is simply a placeholder, dont over think it
## break and continue statements only work on loops, not if statements
## however if they are within an if or elif block, they have to follow the same
## indentations, or else program will not work due to syntax error

