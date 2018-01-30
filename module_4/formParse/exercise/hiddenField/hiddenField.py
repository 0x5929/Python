#!/usr/bin/python


    # this script will execute and enter bogus infomation to hidden fields 

# importing modules

import mechanize
from bs4 import BeautifulSoup



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

br.select_form(nr=0)
    # changing the security value to low
    # for select options, the value must be in a list format
br['security'] = ['low']
    # submitting the value
br.submit()
printFunc(br.title())

    # testing our security level, should yield to ['low']
print "We should now be at the security page"
br.select_form(nr=0)
print "THE SECURITY LEVEL NOW IS: ", br['security']

    # now lets choose to edit the form, and set all the readonly to false
br.set_all_readonly(False)
    # and changing the "hidden form" with name=user_token
br['user_token'] = "HELLO WORLD, I HAVE BEEN CHANGED"
print "BEFORE SUBMISSION, HIDDEN FIELD IS: ", br['user_token']
br.submit()

    # after submission, lets use beautiful soup to see what is hidden value 
bs = BeautifulSoup(br.response().read(), 'lxml')

for inp in bs.find_all('input'):
    if inp['name'] == 'user_token':
        print "AND AFTER SUBMISSION, THE HIDDEN FIELD IS: ", inp['value']
