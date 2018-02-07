#!/usr/bin/python


# this script will be a web spider/crawler
    # TAKES 2 INPUTS: 
        # WEBSITE URL/IP? <-- need to try with test
        # THE DIRECTORY DEPTH FROM THE ROOT DIR
    # EXPECTED OUTPUTS:
        # DOWNLOAD ALL THE HTML FILES FROM EACH DIRECTORY
            # INSERT ALL HTML WITH FIELD AS DIRECTORY NAMES INTO MYSQL DB
        # INSERT ALL THE FORM INFORMATION OF EACH HTML PAGE INTO A SUB TABLE IN MYSQL DB

#   OVERALL GOAL: GATHER ANY WEBSITE DIRECTORIES AND ITS HTML INFO, INCLUDING FORMS ON EACH PAGE 
#                   AND DUMP ALL DATA INTO A MYSQL DB FOR EVALUATION AT A LATER TIME


#   OVERALL DESIGN: 
    # each website enter and parsing is done by individual threads
    # each thread will call outside functions to help dealing with 
    #   linkText/Directory Parsing, and form Parsing, and also DB infrastrcture
    # insert final DB infrastructure to DB, by constructing proper query strings


###############################################################################################################################################
# importing all necessary modules

import threading    # for our thread slaves
import mechanize    # for our web browser
import urllib       # for quick test of response code
import sys          # for system handling
from bs4 import BeautifulSoup   # for parsing the html
# TODO: also need to import mysql db module

# intro system message
print "[!] HELLO WORLD, MY NAME IS CRAWLY AND I AM A WEBSPIDER 0.0"

# grabbing user input
try:    # try block grabbing url and depth count
    url = raw_input("[!] PLEASE ENTER THE WEBSITE'S URL: ")

    if urllib.urlopen(url).code is not 200:     # 200 is ok for http status code
        print "[!] Crawly cannot find the web page, shutting down..."
        sys.exit(1)
    
    depth = raw_input("[!] PLEASE ENTER THE DEPTH COUNT FOR DIRECTORY INFO : ")
    
    try:    # checking if the depth input is correct for interger 
        depth += 1
    except TypeError: 
        print "[!] You have entered a non interger value for the depth count"
        print "[!] Please try again, shutting down..."
        sys.exit(1)

except KeyboardInterrupt:
    print "[!] User has requested a shutdown, shutting down..."
    sys.exit(1)

# setting the input arguments in tuple, and to be passed into the main function
inputArgs = (url, depth)

# global variables
    pass

# function definitions
def evalLink(link):
    pass 
    # evaluate the links in the html page, and looks at all the directories 
    # this will call another thread for each of the sub directories

def depth(browserInstance):
    pass  
    # compare depth global to instance depth 
    # use mechanize browser instance to evaluate links 
        # maybe even calling a evalLink function to do that
    # and this function can just handle if we to crawl deeper, and updates the depth current value

# each thread will have to perform the following tasks
def threadWork(args):
     # grabbing all inputs
    web_url = args[0]
    depth_count = args[1]   
    br = mechanize.Browser()
    br.open(web_url)
    html = br.response().read()
    pass
    # starting mechanize browser
        # connect to url, and get all the html
    # starting beautiful soup parser
        # parses prettified html and saves it to db infra?
    # parse all forms and also saves it to db infra?
    # call depth function with mechanize instance?   

def main(args):
    pass
    # starting the thread workers
    thread_workers = threading.Thread(target=threadWork, args=args) # passing user input as args for each thread
        # rememeber if deeper level is required, please enter the proper args for the main invokation in other functions
    thread.daemon = True    # making sure all thread daemons exit properly after KeyboardInterrupt
    thread.start()  # starting the threads
    # after all thread workers complete given tasks, we need to do db operations to save all to db 

# initial conditions
if __name__ == '__main__':
    main(inputArgs)








