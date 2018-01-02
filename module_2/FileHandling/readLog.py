#!/usr/bin/python


## reading mail log
print "READING MAIL LOG"
maillog = open("/var/log/mail.log", "r")

for line in maillog.readlines():
	print line.strip()

maillog.close()
print "####################################################"


## reading boot log
print "READING BOOT LOG"
bootlog = open("/var/log/boot.log", "r")

for line in bootlog.readlines():
	print line.strip()


bootlog.close()
print "####################################################"


## reading auth log
print "READING AUTH LOG"
authlog = open("/var/log/auth.log", "r")

for line in authlog.readlines():
	print line.strip()


authlog.close()
print "###################################################"


