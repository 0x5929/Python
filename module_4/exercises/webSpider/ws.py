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
import MySQLdb    # mysql database

##############################################################################################################################################


#############################################       INTRO SYSTEM MESSAGE        ##############################################################

print "[!] HELLO WORLD, MY NAME IS CRAWLY AND I AM A WEBSPIDER 0.0"

##############################################################################################################################################


##############################################      GRABBING USER INPUT     ###################################################################

#try:    # try block grabbing url and depth count
#    url = raw_input("[!] PLEASE ENTER THE WEBSITE'S URL: ")
#    try: # testing if type is string for url input
#        url = "http://" + url
#    except TypeError:
#        print "[!] You have entered a non string value for the url"
#        print "[!] Please try again, shutting down..."
#        sys.exit(1)
#
#    if urllib.urlopen(url).code is not 200:     # 200 is ok for http status code
#        print "[!] Crawly cannot find the web page, shutting down..."
#        sys.exit(1)
#    
#    depth = int(raw_input("[!] PLEASE ENTER THE DEPTH COUNT FOR DIRECTORY INFO : "))
#    
#    try:    # checking if the depth input is correct for interger 
#
#        depth = depth + 1
#        depth = depth - 1
#    except TypeError: 
#        print "[!] You have entered a non interger value for the depth count"
#        print "[!] Please try again, shutting down..."
#        sys.exit(1)

#except KeyboardInterrupt:
#    print "[!] User has requested a shutdown, shutting down..."
#    sys.exit(1)
#try:    # try block grabbing url and depth count
#    url = raw_input("[!] PLEASE ENTER THE WEBSITE'S URL: ")
#    try: # testing if type is string for url input
#        url = "http://" + url
#    except TypeError:
#        print "[!] You have entered a non string value for the url"
#        print "[!] Please try again, shutting down..."
#        sys.exit(1)
#
#    if urllib.urlopen(url).code is not 200:     # 200 is ok for http status code
#        print "[!] Crawly cannot find the web page, shutting down..."
#        sys.exit(1)
#    
#    depth = int(raw_input("[!] PLEASE ENTER THE DEPTH COUNT FOR DIRECTORY INFO : "))
#    
#    try:    # checking if the depth input is correct for interger 
#        depth = depth + 1
#        depth = depth - 1
#    except TypeError: 
#        print "[!] You have entered a non interger value for the depth count"
#        print "[!] Please try again, shutting down..."
#        sys.exit(1)

#except KeyboardInterrupt:
#    print "[!] User has requested a shutdown, shutting down..."
#    sys.exit(1)

################################################################################################################################################


##################################################      GLOBAL VARIABLE ASSIGNMENT    ###########################################################

# for developing and testing purpose:
url = 'http://www.github.com/rennitbaby'
depth = 2
# global variables assignment/initialization
base_url = ''
threads = []    
db_html_table = []
db_forms_table = []
directories = {}                                        # data structure: {'1': ['url1', url2], '2': ['url3', 'url4']}
current_depthCount = 1

# setting the input arguments in tuple, and to be passed into the main function
inputArgs = (url, current_depthCount) 

#############################################################################################################################################


#################################################        FUNCTION DEFINITIONS       ########################################################


# url_factory will input a level of depth/directory count
# url_factory will output a list of all urls inside the value list of the level key
def url_factory(level):    
    global base_url             # we will be appending all urls after the base url
    global directories          # we will be using the data inside the directories dictionary, built by dataBuilder called by urlTest called by linkTest, called by linkEval
    ready = []                  # list to be returned to linkEval for resursive call with main
    for url in directories[str(level)]:
        readyUrl = base_url + '/' + url         # appending to the base url with the / added
        ready.append(readyUrl)




# dataBuilder will input a string and a level count
    # dataBuilder will check if the level is avalible
        # if so we check if string is in the list value
            # if so we dont do anything
            # if not we append to the list
        # if not we will add the level count to the dictionary
def dataBuilder(string, lvlCount):
    global directories                                      # initiated at {} as global
    if str(lvlCount) in directories:                        # check if we have the lvl count in directory dictionary
        if string in directories[str(lvlCount)]:            # next we need to check if we have the string in the list value of the lvl count key
            pass                                            # if so, we dont need to do anything, because its already there    
        else:
            directories[str(lvlCount)].append(string)       # if not, lets append it into list value for that lvl count key
    else:                                                   # meaning we dont have the level key in this dictionary yet
        directories[str(lvlCount)] = []                     # initiate the value list
        directories[str(lvlCount)].append(string)           # we will append the url string to the empty value list for the lvl count key



# urlTest will input a full internal url from the html page to be evaulated for further directories or html files
# urlTest will also input an index number to start checking the url page, this is used recursively as we check a long internal url path 
# that has multiple levels
# last input of the function is the level we are at, we will initiate each level at 1 
#   we are going to strip the beginning and the end '/' of each path, since we will append them again individually at the url fac
def urlTest(url, index, level):
    global directories
    dirIndex = url.find('/', index)          # if we can find a / char in the url not including the index which is passed in initially with first linkTest function as 1
    if dirIndex is not -1:                          # string.find() returns -1 if not found
        path = url[:dirIndex]                       # storing the full path up until the / char
            if path[0] == '/':                      # most likely will happen because all paths are relative to root directory
                path = path[1:]                     # so we strip the first initial / char
        dataBuilder(level, path)                    # passing in both the path and the directory level to build the global directory dictionary
        if url.find('/', dirIndex + 1) is not -1:           # if we have another / char after the index level
                                                            # incrmenting the level variable as in this path belongs to the first level
            urlTest(url, dirIndex + 1, level+ 1)            # recursively calling itself with the index of the level to be inspected 
        else:                                               # if we dont have any, and we are at the end
            if url[dirIndex:].endswith('.html')             # checking if we have any files ending with .html for more inspection
                path = url                                  # taking the full path now, because there is no more directories after
                dataBuilder(level + 1, path)                # calling databuilder with this path and level increment because its on the next level
    else:                                                   # this means that the very first check if there is no / other than the first char,
        if url.endswith('.html'):                           # we check for html
            if url[0] == '/':
                path = url[1:]
            dataBuilder(level, path)                        # we invoke databuilder but with the same level, if this is run, should be lvl 1
    

# linkTest function will input a list of tuple with link as first element and url to be evaulated as second  passed in by the linkEval function
    # it will filter for internal links by evaulating the urls, 
    # and split the internal links to either directory links or html links
def linkTest(listofLinks):                                                  # very computational and memory taxing
    urls = []
    directories = []
    htmls = []
    level = 1                                                               # we need to start at the first level with first index for each url check
    index = 1
    for link, url in listofLinks:                                           # filtering for internal urls 
        if url.startswith('http'):                                          # if link start with http
            continue                                                        # next iteration in the for loop
        else:                                                               # internal links
            urls.append((link, url))                                        # appending it to urls list, to be evauated individually with urlTest
    for each_link, each_url in urls:                                        # evaluating each url
        urlTest(each_url, index, level)   


# linkEval function will input a list of url to evaulate 
# linkEval will evaualte the each url -> linkTest -> dataBuilder -> global directories {}
# and check if we need to go deeper, if so we get all the urls ready with urlFac and calls main recursively with deeper level urls
def linkEval(links, current_depth_count):
    global depth                                            # this is user input
    if not links:                                           # test if our current links list if its empty
        print "[!!] THERE IS NO LINKS ON THIS CURRENT HTML PAGE ANYMORE"
        return
    else:
        linkTest(links)                                     # passing it to the linkTest function, to evaluate all links, and append to the data dictionary 
        if current_depthCount >= depth:                     # this means that we are about to exceed our limit, and we dont need to crawl deeper
            return
        else:                                               # this means we still need to crawl deeper with the web spider, and everything under this block is next lvl 
            urls = url_factory(current_depth_count + 1)     # this means we need to grab all url from url_factory that grabs directories with the next level urls        
            for url in urls:
                main(url, current_depth_count + 1)          # recursively calling main with the next level url and updating the depth count for next stack



# dbInfra takes an input of a tuple, with three elements
# url -> type String
# html -> type String
# forms -> type List of tuples or could be empty, if there are no forms on the evaluated page
#   outputs an effect --> appending to the db structure table to be all inserted at the end of the first main call
def dbInfra(args):
    global db_html_table
    global db_forms_table
    url, html, forms = args   
    html_data = (url, 'development html')               # for development, we will only use 'development html' and not the real html
    if not forms:                                       # forms is an empty list on this current evaluated page, then we just append to the html db table
        db_html_table.append(html_data)      
    else:                                               # if forms were available, we will append to html and forms table
        html_data = (url, 'h')                          # appending to html table
        db_html_table.append(html_data)
        for inputTuple in forms:                        # appending to forms table
            Name = inputTuple[0]
            Id = inputTuple[1]
            Type = inputTuple[2]
            Class = inputTuple[3]
            Placeholder = inputTuple[4]
            Disabled = inputTuple[5]
            form_data = (url, Name, Id, Type, Class, Placeholder, Disabled)
            db_forms_table.append(form_data)


# takes in the beautiful soup parsed html from the thread worker, and creates
     # a list of all the form tuple from the html page, and returns it to the threadworker
     # to be worked with by the dbInfra
def formParser(bs):
    forms = []                                              # the returned list of forms 
    inputs = bs.find_all('input')                           # this returns a list of all inputs on the bs parsed html
    for eachInput in inputs:                                # for each of the inputs, we will append a tuple of the following attr
        Name = eachInput.get('name')
        Id = eachInput.get('id')
        Type = eachInput.get('type')
        Class = eachInput.get('class')
        Value = eachInput.get('value')
        Placeholder = eachInput.get('placeholder')
        Disabled = eachInput.get('disabled')
        forms.append((Name, Id, Type, Class, Value, Placeholder, Disabled))
    return forms                                            # outputs a list of tuples full of each input form's info


# takes in the browser instance from the thread worker, and creates
# a list of link urls to be evaluated later by another of the thread's function 
# from the html page and returns it to the threadworker for more evaluation
def linkParser(brInstance):   
    links = []
    try:    # just in case if br.Instance.links() return type None 
        for link in brInstance.links():
            links.append(link.url)
    except: 
        return links
    finally:
        return links


# takes an browser instance as arg, and spits out pretty html to the thread worker
def htmlParser(brInstance):  
    html = brInstance.response().read()
    workHtml = BeautifulSoup(html, 'lxml')
    prettyHtml = workHtml.prettify()
    return (prettyHtml, workHtml)


# each thread will have to perform the following tasks
    #takes input of url, and parses the html, forms, and links with help of various other functions
def threadWork(args):                               
    web_url = args[0]                                   # grabbing all inputs
    current_depth_lvl = args[1]
    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.open(web_url)
    dbHtml, workHtml = htmlParser(br)                   # passing in the browser at the current state to html link parsers to retrieve info
    forms = formParser(workHtml)                        # html and forms is going to be used for db insertion
    links = linkParser(br)                  
    br.close()                                          # closing the browser, since we have no more work for it in this thread worker
    dbInfra((web_url, dbHtml, forms))
    linkEval(links, current_depth_lvl)                  # evaluating links, will invoke linkTest --> urlTest --> dataBuilder --> update global directories {}
                                                        # will test against global depth, with currentDepthLvl if needed invokes url_factory for urls 
                                                        # to be called recursivly with main but increments the depthcount


# threadStarter function will input a index for the current thread in the global threads list appended by the threadworker
#   and start the thread
# we need to join all threads and starting them
def threadStarter(i):   
    global threads
    current_thread = threads[i]
    current_thread.daemon = True
    current_thread.start()
    current_thread.join()


def main(args):
    global threads
    # starting the thread workers
    thread_worker = threading.Thread(target=threadWork, args=args) # passing user input as args for each thread
        # rememeber if deeper level is required, please enter the proper args for the main invokation in other functions
    threads.append(thread_worker)
    index = threads.index(thread_worker)
    threadStarter(index)
    # after all thread workers complete given tasks, we need to do db operations to save all to db 


# baseUrl will input a url (user input)
# baseUrl will update the global variable of base_url
def baseUrl(fullUrl):
    global base_url
    httpIndex = len('http://')                               # grabbing the index of http://, if for exclusive range, we need to take index + 1, which is the full length
    if fullUrl.find('/', httpIndex) == -1:                   # we only want start checking if we have another / after http://
        base_url = fullUrl                                   # if we dont have another / after http:// the full url is the base url
    else:                                                    # if we do have another /, then the base url is the whole thing until that found /
        index = fullUrl.find('/', httpIndex)
        base_url = fullUrl[:index]                           # base url is the full url up until the found /, note not including /


def db_operations():
    global threads
    global db_html_table
    global db_forms_table
    ## do database operations: INSERT
    print db_html_table
    print "="*100
    print db_forms_table
    print threads
    pass

################################################################################################################################################


#################################################       SCRIPT EXECUTION        ################################################################

if __name__ == '__main__':
    baseUrl(url)                    # this is to update the global value of baseUrl to be used for url_factory link appending purposes
    main(inputArgs)                 # main function --> executes thread workers --> executes db infra, and crawls deeper if needed
    db_operations()                 # database operations, for db insertion at the very end

################################################################################################################################################





