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


##############################################      IMPORTING MODULES       ###################################################################

import threading    # for our thread slaves
import mechanize    # for our web browser
import urllib       # for quick test of response code
import sys          # for system handling
from bs4 import BeautifulSoup   # for parsing the html
import mysql    # mysql database

##############################################################################################################################################


#############################################       INTRO SYSTEM MESSAGE        ##############################################################

print "[!] HELLO WORLD, MY NAME IS CRAWLY AND I AM A WEBSPIDER 0.0"

##############################################################################################################################################


##############################################      GRABBING USER INPUT     ###################################################################

try:    # try block grabbing url and depth count
    url = raw_input("[!] PLEASE ENTER THE WEBSITE'S URL: ")
    try: # testing if type is string for url input
        url = "http://" + url
    except TypeError:
        print "[!] You have entered a non string value for the url"
        print "[!] Please try again, shutting down..."
        sys.exit(1)

    if urllib.urlopen(url).code is not 200:     # 200 is ok for http status code
        print "[!] Crawly cannot find the web page, shutting down..."
        sys.exit(1)
    
    depth = raw_input("[!] PLEASE ENTER THE DEPTH COUNT FOR DIRECTORY INFO : ")
    
    try:    # checking if the depth input is correct for interger 
        depth = depth + 1
        depth = depth - 1
    except TypeError: 
        print "[!] You have entered a non interger value for the depth count"
        print "[!] Please try again, shutting down..."
        sys.exit(1)

except KeyboardInterrupt:
    print "[!] User has requested a shutdown, shutting down..."
    sys.exit(1)

#############################################################################################################################################


##################################################      VARIABLE DECLARATIONS AND INITIALIZATION    #########################################
# setting the input arguments in tuple, and to be passed into the main function
inputArgs = (url, depth)

# global variables declaration/initialization
threads = []    
db_html = {}
db_forms = {}

#############################################################################################################################################


#################################################        FUNCTION DEFINITIONS       ########################################################

# evalLink function will take an input of a list full of links on the html page
# this will evaulate each link and determine the directory details of the webserver folder
def evalLink(links):
    urls = []
    for url in links:   # filters through all the links for the internal ones
        if url.startswith('http'):
            continue    # next iteration in the for loop
        else:   # internal links
            urls.append(url)
    ans = directory(urls)  # passing it to the directory function to look for directories in the internal url

         # SAME GOES FOR THE LOWER LEVEL FUNCTIONS CHECKING FOR URL IN A PAGE 
    dirs = ans[0]   # we need to compare with depth value to see if we should go into any more directories. 
    htmlUrl = ans[1]  # we need to parse all of the html by calling main on each of the html urls
                        # REMEMBER, THESE URLS ARE RELATIVE, SO WE NEED TO ADD THE CURRENT URL AND DIRECTORIES, 
                        # UPDATE THE GLOABL URL ARG, AND UPDATE THE DEPTH COUNT TO 0 TO INVOKE MAIN

        # REMEMBER TO CHECK THE VALUES BELOW IF ITS EMPTY OR NOT, IF EMPTY WE STOP THE OPERATION
    if not dirs:
        print "NO MORE DIRECTORIES" # NEED TO HANDLE THIS
    if not htmls:
        print "NO MORE HTML PAGES IN THE CURRENT DIRECTORY" # ALSO NEED TO HANDLE THIS
    pass 
    # evaluate the links in the html page, and looks at all the directories 
    # this will call another thread for each of the sub directories

def directory(listofURLs):  # very computational and memory taxing
    directories = []
    htmls = []
    for url in listofURLs:
        for i in range(1, len(url)):    # iterating through each characters in the url
            if url[i] == '/':   # this has to mean its a directory
                directories.append(url[:i+1])  #   appending the whole url up to the first '/' char
            else if url.endswith('.html'):  # this means its another html page in the same directory and needs to be parsed
                htmls.append(url)   # we will append the full url, because it doesnt have '/' in it, and it ends with html, so relative to / 
    answer = (directories, htmls)
    return answer

def depth(dirUrl):

    pass  
    # compare depth global to instance depth
    # use mechanize browser instance to evaluate links 
        # maybe even calling a evalLink function to do that
    # and this function can just handle if we to crawl deeper, and updates the depth current value

def formParser(brInstance): # takes in the browser instance from the thread worker, and creates
                            # a list of all the form obj from the html page, and returns it to the threadworker
                            # need to have a better way to parse the forms, in order to put inside db, need to rewatch the question video
    forms = []
    for form in brInstance.forms():
        forms.append(form)
    return forms

def linkParser(brInstance):     # takes in the browser instance from the thread worker, and creates
                                # a list of all the link urls from the html page and returns it to the threadworker for more evaluation
    links = []
    for link in brInstance.links():
        links.append(link.url)
    return links

def htmlParser(html):   # takes an browser instance as arg, and spits out pretty html to the thread worker
    html = brInstance.reponse().read()
    prettyHtml = BeautifulSoup(html, 'lxml').prettify()
    return prettyHtml

# each thread will have to perform the following tasks
def threadWork(args):
     # grabbing all inputs
    web_url = args[0]
    depth_count = args[1]   
    br = mechanize.Browser()
    br.open(web_url)
    # passing in the browser at the current state to form and link parsers to retrieve info
    forms = formParser(br)
    links = linkParser(br)
    linkEval(links) # evaluating links, and will invoke depth calculations in linkEval function as well
    # below html is going to be used for db insertion, maybe pass it into another function to rearrange 
    html = htmlParser(br)
    pass
    # starting mechanize browser
        # connect to url, and get all the html
    # starting beautiful soup parser
        # parses prettified html and saves it to db infra?
    # parse all forms and also saves it to db infra?
    # call depth function with mechanize instance?   

def threadStarter():
    for thread in threads:
        thread.daemon = True    # making sure all thread daemons exit properly after KeyboardInterrupt
        thread.start()  # starting the thread
        thread.join()   # making sure all threads are finished before continuing execution in main
        threads.remove(thread)  # remove thread from the thread list, so it wont be started again

def main(args):
    # starting the thread workers
    thread_workers = threading.Thread(target=threadWork, args=args) # passing user input as args for each thread
        # rememeber if deeper level is required, please enter the proper args for the main invokation in other functions
    threads.append(thread_workers)
    threadStarter()
    # after all thread workers complete given tasks, we need to do db operations to save all to db 
    pass

def db_operations():
    pass

################################################################################################################################################


#################################################       SCRIPT EXECUTION        ################################################################

if __name__ == '__main__':
    main(inputArgs)
    db_operations()

################################################################################################################################################






