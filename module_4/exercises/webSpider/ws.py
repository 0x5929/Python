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

#############################################################################################################################################


##################################################      VARIABLE DECLARATIONS AND INITIALIZATION    #########################################
# setting the input arguments in tuple, and to be passed into the main function
#inputArgs = (url,) 

# for developing and testing purpose:
url = 'http://www.github.com/rennitbaby'
depth = 2
inputArgs = (url,) 
# global variables declaration/initialization
threads = []    
db_html_table = []
db_forms_table = []
directories = {}
current_depthCount = 1

#############################################################################################################################################


#################################################        FUNCTION DEFINITIONS       ########################################################


# url_appender function will append the the directoryUrls, and htmlUrls, to the currently modifying path
#   also it will update the current count of depth count before outputting a tuple of lists of both resulting appended urls
def url_factory(directoryLinks, htmlLinks, brInstance):    # this will evaluate the depth count
    global current_depthCount
    readyDirUrl = []
    readyHtmlUrl = []
    # testing if input args are avaliable
    if not directoryLinks: 
        # remember if these input lists are empty that means there is no html or dir links on the current evaualted html page
        # and that means even if we need to crawl deeper, we cannot do so anymore, and we would send an emtpy list back to link_eval, 
        # to not call Main(), and stops execution of the current thread
        pass
    else: 
        for dirLink in directoryLinks:    # appending the current url to the relative urls
            brInstance.follow_link(dirLink)
            dirUrl = brInstance.geturl()
            readyDirUrl.append(dirUrl)
    if not htmlLinks:
        pass
    else:
        for htmlLink in htmlLinks:
            brInstance.follow_link(htmlLink)
            htmlUrl = brInstance.geturl()
            readyHtmlUrl.append(htmlUrl)
    ready = (readyDirUrl, readyHtmlUrl)
    # we need to increment the depth count
    current_depthCount += 1
    # closing the browser instance
    brInstance.close()
    return ready

def dicTest(count):
    if count > 0:  # count has to be bigger than 0
        

    pass

def dataBuilder(string, lvlCount):
    global directories
    




    if lvlCount > 0 : # count has to be bigger than 0
        dictTest(lvlCount)
    else:
        
    pass

# urlTest will input a url, and we will iterate through each of the character to build the global dictionary of directory listings
def urlTest(url, index, level):
    global directories
    # iterate through each character for / but not the first one
    dirIndex = url.find('/', 1) # if we can find a / char in the url not including the first 1
    path = url[:dirIndex]   # storing the full path up until the / char
    dataBuilder(level, path)    # passing in both the path and the directory level to build the global directory dictionary
    if url.find('/', dirIndex + 1):  # if we have another / char after the index level
        level += 1  #   incrmenting the level variable as in this path belongs to the first level
        urlTest(url, dirIndex + 1, level)  # recursively calling itself with the index of the level to be inspected 
    else:   # if we dont have any, and we are at the end
        if url[dirIndex:].endswith('.html') # checking if we have any files ending with .html for more inspection
            path = url[dirIndex + 1:]
            dataBuilder(level, path)    # calling databuilder with this path and level
        return
    
    
    
    
    for i in range(len(url)):
        dirIndex = url[1:].index('/')  + 1 
        
        
        if i is not 0 and url[i] == '/':    # this means a directory, and not counting the first '/'
            # remember the splice rule is inclusive:exclusive
            directoryString = url[:i]
            if directoryString[0] == '/':   # if the first character is a / char, which means root directory, we just need the words
                directoryString = directoryString[1:]
            dictionaryBuilder(directoryString, count)  # calls directoryBuilder with the string, and level count
            try:    # this is if there is more to the url link
                url = url[i+1:]
                # update count and call urlTest self recursively
                count += 1
                urlTest(url, count)
            except IndexError:     # this is when there is no more url after the / char, means we are done with this url
                return                
        elif i == len(url) - 1 and \
                url[i] is not '/' and\
                url.endswith('.html'):
                    # this means, we have reached the end of our char interation of the string, and 
                    # we still havent found a / char, we will see if the current url end in .html, so they can be passed into main to be parsed
                    htmlString = url[:i]
                    if htmlString[0] == '/':    # gets rid of the inital / char
                        htmlString = htmlString[1:]
                    dictionaryBuilder(htmlString, count)
    pass


# linkTest function will input a list of tuple with link as first element and url to be evaulated as second  passed in by the linkEval function
    # it will filter for internal links by evaulating the urls, 
    # and split the internal links to either directory links or html links
def linkTest(listofLinks):  # very computational and memory taxing
    urls = []
    directories = []
    htmls = []
    for link, url in listofLinks:          # filtering for internal urls 
        if url.startswith('http'):
            continue    # next iteration in the for loop
        else:   # internal links
            urls.append((link, url))

    for each_link, each_url in urls:
        # first arg is the full url relative to /, second arg is index we start at: 1, third is the level we start at for each url: 1
        # urlTest(each_url, 1, 1)   
        # done loop
    # new_urlFactory()
        for i in range(1, len(each_url)):    # iterating through each characters in the url
            if each_url[i] == '/':   # this has to mean its a directory
                directories.append(each_link)  #  appending the link that is associated with the direcotry link url
            elif each_url.endswith('.html'):  # this means its another html page in the same directory and needs to be parsed
                htmls.append(each_link)   # appending the link associated with the html link url

    answer = (directories, htmls)

    return answer


# linkEval function will input a list of tuples with link obj as first element and url to evaulate as second argument 
# on the html page we are inspecting,  and the browser instance opened by the threadworker, 
# we will use the browser to follow each of the link object associate with each internal links 
# and get the full url to be the ones we will pass in for the recursive main function call links for furthur inspection or return with no actions needed
# which depends on a test within linkEval
# this will evaulate each link and determine the directory details of the webserver folder
def linkEval(links, brInstance):
    global current_depthCount
    # test if our current links list if its empty
    if not links:
        # there is no links on the current evaluated html page
        print "[!!] THERE IS NO LINKS PASSED INTO THE LINK EVALUATION FUNCTION BY THE THREADWORKER, PARSED ON THIS CURRENT HTML PAGE"
        return
    else:
        print "#"*50 + "" + "#"*50
        dirLinks, htmlLinks = linkTest(links)  # passing it to the directoryTest function to look for directories and html links in the links parsed by threadworker
        print "#"* 50 + "link eval after link test" + "#" *50 
        print dirLinks
        print htmlLinks
        if current_depthCount >= depth: # this means that we are about to exceed our limit, and we dont need to crawl deeper
            return
        else:              
        # first we need to call the function to evalate depth, and returns tuple of list of urls to pass into the main 
            readyDirUrls, readyHtmlUrls = url_factory(dirLinks, htmlLinks, brInstance)
        # we need to call main again with all the urls, both dirs, and html
            print "#"*50 + "readyDirlUrls and readyHtmlUrls after url APpender" + "#"*50
            print readyDirUrls
            print readyHtmlUrls
            print "#"* 100
            for dirUrl in readyDirUrls:
                main((dirUrl,))
            for htmlUrl in readyHtmlUrls:
                main((htmlUrl,))


# dbInfra takes an input of a tuple, with three elements
# url -> type String
# html -> type String
# forms -> type List of objects or could be empty, if there are no forms on the evaluated page
#   outputs an effect --> appending to the db structure table to be all inserted at the end of the first main call
def dbInfra(args):
    global db_html_table
    global db_forms_table
    url, html, forms = args
    
    if not forms:
        # forms is an empty list on this current evaluated url, then we just append to the html db table
        html_data = (url, 'h')
        db_html_table.append(html_data)
    else:
        # if forms were available, we will append to html and forms table
        # appending to html table
        html_data = (url, 'h')
        db_html_table.append(html_data)
        # appending to forms table
        for form in forms:
            form_data = (url, form)
            db_forms_table.append(form_data)


# takes in the browser instance from the thread worker, and creates
     # a list of all the form obj from the html page, and returns it to the threadworker
def formParser(brInstance):
    forms = []
    try:    # just in case if brInstance.forms() return type None
        for form in brInstance.forms():
            forms.append(form)
    except:
        return forms
    finally:
        return forms

# takes in the browser instance from the thread worker, and creates
# a list of tuple with all the link as first element and all the urls for the second element of tuple
# from the html page and returns it to the threadworker for more evaluation
def linkParser(brInstance):   
    links = []
    try:    # just in case if br.Instance.links() return type None 
        for link in brInstance.links():
            links.append((link, link.url))
    except: 
        return links
    finally:
        return links


# takes an browser instance as arg, and spits out pretty html to the thread worker
def htmlParser(brInstance):  
    html = brInstance.response().read()
    prettyHtml = BeautifulSoup(html, 'lxml').prettify()
    return prettyHtml


# each thread will have to perform the following tasks
    #takes input of url, and parses the html, forms, and links with help of various other functions
def threadWork(args):
     # grabbing all inputs
    web_url = args
    print 'hello, we are here'
    print web_url
    br = mechanize.Browser()
    br.set_handle_robots(False)
    if web_url == 'https://github.com/rennitbaby/Select_Therapy_Web_App':
        print 'HELLLLLLLLO testing'
        print br
    try:
        br.open(web_url)
    except:
        print "TESTING WHAT IS GOING ON"
    print "WHY DOES THIS NOT GET PRINTED AFTER THE SECOND THREAD"
    print br
    # passing in the browser at the current state to form and link parsers to retrieve info
    # below html and forms is going to be used for db insertion, maybe pass it into another function to rearrange 
    html = htmlParser(br)
    forms = formParser(br)
    links = linkParser(br)
    dbInfra((web_url, html, forms))
    linkEval(links, br) # evaluating links, and will invoke see if we need to crawl deeper, and calls main again recursively if we do need to crawl deeper


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
    pass

def db_operations():
    global threads
    global db_html_table
    global db_forms_table
    print db_html_table
    print "="*100
    print db_forms_table
    print threads
    pass

################################################################################################################################################


#################################################       SCRIPT EXECUTION        ################################################################

if __name__ == '__main__':
    main(inputArgs)
    db_operations()

################################################################################################################################################






