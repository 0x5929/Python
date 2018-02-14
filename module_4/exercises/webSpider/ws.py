#!/usr/bin/python


##                      this script will be a web spider/crawler

#                        TAKES 2 INPUTS: 
#                         WEBSITE URL/IP
#                         THE DIRECTORY DEPTH FROM THE ROOT DIR

#                       EXPECTED OUTPUTS:
#                        DOWNLOAD ALL THE HTML FILES FROM EACH DIRECTORY
#                        INSERT ALL HTML WITH FIELD AS DIRECTORY NAMES INTO MYSQL DB
#                        INSERT ALL THE FORM INFORMATION OF EACH HTML PAGE INTO ANOTHER  TABLE IN MYSQL DB

#   OVERALL GOAL: GATHER ANY WEBSITE DIRECTORIES AND ITS HTML INFO, INCLUDING FORMS ON EACH PAGE 
#                   AND DUMP ALL DATA INTO A MYSQL DB FOR EVALUATION AT A LATER TIME


#   OVERALL DESIGN: 
    # each website enter and parsing is done by individual threads
    # each thread will call outside functions to help dealing with 
    #   linkText/Directory Parsing, and form Parsing, and also DB infrastrcture
    # insert final DB infrastructure to DB, by constructing proper query strings


###############################################################################################################################################


##############################################      IMPORTING MODULES       ###################################################################

import threading                    # for our thread slaves
import mechanize                    # for our web browser
import urllib                       # for quick test of response code
import sys                          # for system handling
from bs4 import BeautifulSoup       # for parsing the html
import MySQLdb                      # mysql database

##############################################################################################################################################


#############################################       INTRO SYSTEM MESSAGE        ##############################################################

print "\n[!] HELLO WORLD, MY NAME IS CRAWLY AND I AM A WEBSPIDER 0.0"

##############################################################################################################################################


##############################################      GRABBING USER INPUT     ###################################################################

#try:                                                               # try block to grab url and depth count
#    url = raw_input("[!] PLEASE ENTER THE WEBSITE'S URL: ")
#    try:                                                           # testing if type is string for url input
#        url = "http://" + url
#    except TypeError:
#        print "[!] You have entered a non string value for the url"
#        print "[!] Please try again, shutting down..."
#        sys.exit(1)
#
#    if urllib.urlopen(url).code is not 200:                        # 200 is ok for http status code
#        print "[!] Crawly cannot find the web page, shutting down..."
#        sys.exit(1)
#    
#    depth = int(raw_input("[!] PLEASE ENTER THE DEPTH COUNT FOR DIRECTORY INFO : "))
#    
#    try:                                                           # checking if the depth input is correct for interger 
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


# INPUT: url_factory will input a level of depth/directory count
# OUTPUT: url_factory will output a list of all urls inside the value list of the level key
def url_factory(level):    
    global base_url                                 # we will be appending all urls after the base url
    global directories                              # we will be using the data inside the directories dictionary, 
                                                    # built by dataBuilder called by urlTest called by linkTest, called by linkEval
    ready = []                                      # list to be returned to linkEval for resursive call with main
    for url in directories.get(str(level), []):     # default to [] if dictionary does not have the key, and will return empty [] to control
        readyUrl = base_url + '/' + url             # appending to the base url with the / added
        ready.append(readyUrl)
    return ready




# INPUT: dataBuilder will input a string and a level count
# OUTPUT: no return value, but will build up the global directories dictionary with series of tests
def dataBuilder(string, lvlCount):
    global directories                                      # initiated at {} as global
    #print string, lvlCount
    if str(lvlCount) in directories:                        # check if we have the lvl count in directory dictionary
        if string in directories[str(lvlCount)]:            # next we need to check if we have the string in the list value of the lvl count key
            pass                                            # if so, we dont need to do anything, because its already there    
        else:
            directories[str(lvlCount)].append(string)       # if not, lets append it into list value for that lvl count key
    else:                                                   # meaning we dont have the level key in this dictionary yet
        directories[str(lvlCount)] = []                     # initiate the value list
        directories[str(lvlCount)].append(string)           # we will append the url string to the empty value list for the lvl count key




# INPUT: urlTest will input a full internal url from the html page to be evaulated for further directories or html files
#       urlTest will also input an index number to start checking the url page, this is used recursively as we check a long internal url path 
#       that has multiple levels until there are no more / char indicating directories in the url string
#       last input of the function is the level we are at
#       we will initiate each url string with level at 1 (if repeated, will be checked by dataBuilder)
# OUTPUT: no return value but will send string and level count to dataBuilder for checks and append to the global directories {}
def urlTest(url, index, level):
    print '*'*50
    print 'url: ', url
    print 'index: ', index
    print 'level: ', level
    print '*'*50
    global directories
    dirIndex = url.find('/', index)                 # if we can find a / char in the url not including the index which was 
                                                    # passed in initially with first linkTest function as 1
    if dirIndex == -1:                               # means there is no / after the initial root /
    #current lvl count is initiated at 1
    #  if we do have a dirIndex meaning / after initial one:
    #   we set the path to url up until the second /
    #   and send it to dataBuilder with current count lvl, this case is 1
    #   recurvively calling with same url, the new index at the dirIndex + 1, then increment the lvl count
    #   and then we check for more url after this one, if we have another /
    # else we dont have a /
    #   lvl count is 1
    #   we would want these things:
    #   1. if it ends with .html    
    #   2. filter through all the files that dont have a dot . in it
    #   3. send 1 and 2 to databuilder with lvl count of current, this case is 1 
    
    
    
    if dirIndex is not -1:                          # meaning we found the second / string.find() returns -1 if not found
        path = url[:dirIndex]                       # storing the full path up until the / char
        if path[0] == '/':                          # most likely will happen because all paths are relative to root directory
            path = path[1:]                         # so we strip the first initial / char
        dataBuilder(path, level)                    # passing in both the path and the directory level to build the global directory dictionary
                                                            # incrmenting the level variable and incrementing index variable so 
        urlTest(url, dirIndex + 1, level+ 1)                # recursively calling itself with the index of the level to be inspected 
   #     else:                                               # if we dont have any, and we are at the end
    #        if url[dirIndex:].endswith('.html'):            # checking if we have any files ending with .html for more inspection
     #           path = url                                  # taking the full path now, because there is no more directories after
      #          dataBuilder(level + 1, path)                # calling databuilder with this path and level increment because its on the next level
    else:                                                   # this means that the very first check if there is no / other than the first char,
        if url.endswith('.html'):                           # we check for html
            if url[0] == '/':
                path = url[1:]
            dataBuilder(path, level)                        # we invoke databuilder but with the same level, if this is run, should be lvl 1
        elif '.' in url and not url.endswith(".html"):                                    # if we have . and we are not html, 
            pass
        else:                                                                             # this is what we want
            if url[0] == '/':
                path = url[1:]
            dataBuilder(path, level)


# INPUT:  linkTest function will input a list of urls passed in by the linkEval function
# OUTPUT: no return value from linkTest, but initiate urlTest for each internal urls
#          to be broken down and sent to dataBuilder to be evaluated and appended if needed to the global directories dictionary 
def linkTest(listofLinks):                                                 
    urls = []
    level = 1                                                               
    index = 1                                                               # we need to start at the first level with first index 
                                                                            # for each url check
    for url in listofLinks:                                                 # filtering for internal urls 
        if url.startswith('http'):                                          # if link start with http
            continue                                                        # next iteration in the for loop
        else:                                                               # internal links
            urls.append(url)                                                # appending it to urls list, to be evauated individually with urlTest
    print urls
    for each_url in urls:                                                   # evaluating each url
        urlTest(each_url, index, level)   




# INPUT: linkEval function will input a list of url to evaulate passed in by each thread worker
# OUTPUT: no return value but linkEval will evaualte the each url through -> linkTest -> urlTest -> dataBuilder -> global directories {}
#          and check if we need to go deeper, if so, we get all the urls ready with urlFac and calls main recursively with deeper level urls
def linkEval(links, current_depth_count):
    global depth                                            # this is user input
    if not links:                                           # test if our current links list if its empty
        print "[!!] THERE IS NO LINKS ON THIS CURRENT HTML PAGE ANYMORE"
        return
    else:
        linkTest(links)                                     # passing it to the linkTest function, to evaluate all links 
        if current_depthCount >= depth:                     # this means that we are about to exceed our limit, and we dont need to crawl deeper
            return
        else:                                               # this means we still need to crawl deeper with the web spider, 
                                                            # and everything under this block is next lvl 
            urls = url_factory(current_depth_count + 1)     # this means we need to grab all url from url_factory 
                                                            # that grabs directories with the next level urls        
            for url in urls:
                main((url, current_depth_count + 1))        # recursively calling main with the next level url
                                                            # and updating the depth count for next stack




# INPUT:  dbInfra takes an input of a tuple, with three elements
#          url -> type String
#          html -> type String
#          forms -> type List of tuples or could be empty, if there are no forms on the evaluated page
# OUTPUT: dbInfra will appendto the global db structure table to be all inserted at the end of the first main call
def dbInfra(args):
    global db_html_table
    global db_forms_table
    url, html, forms = args   
    html_data = (url, 'development html')               # for development, we will only use 'development html' and not the real html
    if not forms:                                       # forms is an empty list on this current evaluated page, 
                                                        # then we just append to the html db table
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




# INPUT: formParser takes in an input of beautiful soup parsed html from the thread worker
# OUTPUT: formParser will return a list of tuples of each input form detail in order
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


# INPUT: takes in the browser instance from the thread worker
# OUTPUT: returns a list of link urls to be evaulated with linkEval in the threadworker execution
def linkParser(brInstance):   
    links = []
    try:                                                    # just in case if br.Instance.links() return type None 
        for link in brInstance.links():
            links.append(link.url)
    except: 
        return links
    finally:
        return links


# INPUT: takes an browser instance as arg, 
# OUTPUT: returns a tuple with a html to be insert to db structure, and another html to be worked with in formParse
def htmlParser(brInstance):  
    html = brInstance.response().read()                     # grabbing the html response from the mechanize browser instance
    workHtml = BeautifulSoup(html, 'lxml')                  # parsing using lxml parser
    prettyHtml = workHtml.prettify()                        # using prettify method from beautifulSoup to make html more readable
    return (prettyHtml, workHtml)

# INPUT: inputs tuple of url and current depth lvl (initated at lvl 1) from the main function where thread is defined 
# OUTPUT: no return value, but each thread will have to perform the following tasks
def threadWork(args):                               
    web_url = args[0]                                   # grabbing all inputs
    current_depth_lvl = args[1]                         
    br = mechanize.Browser()                            # starting the mechanize browser instance
    br.set_handle_robots(False)                         # make sure we are robot.txt friendly
    br.open(web_url)                                    # using the browser instance to open the url passed in
    dbHtml, workHtml = htmlParser(br)                   # passing in the browser at the current state to html parser to retrieve htmls
    links = linkParser(br)                              # passing the browser at the current state to the link parser to retrieve links 
    forms = formParser(workHtml)                        # passing in the working html for formParser to get parsed forms 
    br.close()                                          # closing the browser, since we have no more work for it in this thread worker
    dbInfra((web_url, dbHtml, forms))                   # passing url, and all parsed info to the dbInfra to build db structure 
    linkEval(links, current_depth_lvl)                  # evaluating links, will invoke linkTest --> urlTest --> dataBuilder --> 
                                                        # update global directories {}
                                                        # linkEval will test against global depth, with currentDepthLvl 
                                                        # if needed invokes url_factory for urls 
                                                        # to be called recursivly with main but increments the depthcount




# INPUT: threadStarter will input a index for the current thread in the global threads list appended by the threadworker
# OUTPUT: no return value but threadStarter will start set the daemon, start, and join the thread
def threadStarter(i):   
    global threads
    current_thread = threads[i]
    current_thread.daemon = True
    current_thread.start()
    current_thread.join()


# INPUT: main will input a tuple of url and current depth count
# OUTPUT: no return value, but main will invoke threadStarter, which will start each thread, called on the first and recursively
def main(input_args):
    global threads
    thread_worker = threading.Thread(target=threadWork, args=(input_args,))                 # passing user input as args for each thread
    threads.append(thread_worker)                                                           # appending to global thread list
    index = threads.index(thread_worker)                                                    # finding out what index the thread is
    threadStarter(index)                                                                    # calling threadStarter with the thread index




# INPUT: baseUrl will input a url (user input)
# OUTPUT: no return value but baseUrl will update the global variable of base_url
def baseUrl(fullUrl):
    global base_url
    httpIndex = len('http://')                               # grabbing the index of http://, for exclusive range
                                                             # we need to take index + 1, which is the full length
    if fullUrl.find('/', httpIndex) == -1:                   # we only want start checking if we have another / after http://
        base_url = fullUrl                                   # if we dont have another / after http:// the full url is the base url
    else:                                                    # if we do have another /, then the base url is the whole thing until that found /
        index = fullUrl.find('/', httpIndex)
        base_url = fullUrl[:index]                           # base url is the full url up until the found /, note not including /




# INPUT: db_operations require no input
# OUTPUT: no return value, but db_operations will perform mysql db operations and insert all found data to the db
def db_operations():
    global db_html_table
    global db_forms_table
    ## do database operations: INSERT
    print db_html_table
    print "="*100
    print db_forms_table




################################################################################################################################################


#################################################       SCRIPT EXECUTION        ################################################################

if __name__ == '__main__':
    baseUrl(url)                    # this is to update the global value of baseUrl to be used for url_factory link appending purposes
    main(inputArgs)                 # main function --> executes thread workers --> executes db infra, and crawls deeper if needed
    db_operations()                 # database operations, for db insertion at the very end
    print "\n[!] Crawly the web spider is now complete with all of his tasks, shutting down..."
    sys.exit(0)                     # gracefully exits the system

################################################################################################################################################





