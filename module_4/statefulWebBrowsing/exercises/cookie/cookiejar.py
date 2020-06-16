#!/usr/bin/python


# this script will do two of the following things:
    # first: we will try to implement the cookies into a mechanize browser and test it by reenter the page, and we should be logged in
    # second: we will try to copy the existing cookie into a cookiejar and use it for another mechanize broswer instance to be tested

import mechanize

##########################################                  SETUP

# creating the browser
br = mechanize.Browser()

# this will be used for the second objective
    # creating cookie jar instance obj
cj = mechanize.CookieJar()
# setting the cookie jar to the first browser, thus all of the first browser cookies will be placed in this cookie jar 
    # so we can pass it onto our second browser instance br1
br.set_cookiejar(cj)
# having the browser to navigate to a specific website that we already have cookies for 
br.open("http://localhost/DVWA")    # we have to now set the cookies, and the expiration, referenced from the mechanize docs
br.set_cookie("PHPSESSID=m77lto4kcp4g0v4ce234kkt7cg; expires=Wednesday, 31-Jan-18 00:00:00 GMT")
br.set_cookie("security=low; expires=Wednesday, 31-Jan-18 00:00:00 GMT")

# now for the second objective, we are creating another browser instance 
# and setting the cookie jar of the second instance with the same cookie jar as the first one
br1 = mechanize.Browser()
br1.set_cookiejar(cj)   # setting the first browser cj to the second browser

########################################                TEST
# this is the first test
print "testing if the first inputted cookies are set for the first browser instance"
br.open('http://localhost/DVWA')
print br.title()

if "Welcome" in br.title():
    print "##we passed the first test##"
else:
    print "##first test failed##"


# this is the second test
print "now testing if the second browser also received the cookiejar from the first browser instance"
br1.open("http://localhost/DVWA")
print br1.title()

if "Welcome" in br1.title():
    print "##we also passed the second test##"
else:
    print "##Oops, second test failed##"
