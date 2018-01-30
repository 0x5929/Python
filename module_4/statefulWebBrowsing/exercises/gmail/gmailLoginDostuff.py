#!/usr/bin/python

# importing modules

import mechanize
from bs4 import BeautifulSoup
from datetime import datetime

# defining the print url function
def printURL(url, title):
    print "#"* 100
    print datetime.now()
    print "CURRENT URL: ", url
    print "CURRENT TITLE: ", title
    print "#"* 100

# starting the browswer

br = mechanize.Browser()
# we need to make sure we are not seen as a robot by the website
br.set_handle_robots(False)
br.open('https://www.gmail.com')
printURL(br.geturl(), br.title())

# lets see all the forms in the this page
#for form in br.forms():
#    print form
# there is only one form on this page
    # lets log in
br.select_form(nr=0)
br['Email'] = 'work.kevin.ren@gmail.com'
#br['password'] = 'password'
br.submit()
    # lets see where we are at
printURL(br.geturl(), br.title())

# lets see what forms we have here: 
#for form in br.forms():
#    print form

# there are only one form, lets fill out the Passwd field
br.select_form(nr=0)
br['Passwd'] = 'jordan45'
br.submit()
    
    # lets see where we are at
printURL(br.geturl(), br.title())
    
    # lets print out the parsed html using beautifulsoup
bs = BeautifulSoup(br.response().read(), 'lxml')
#print bs.prettify()
    # lets print out all the links
for link in br.links():
    try: 
        print link.url + " :  " + link.text
    except: 
        pass

# lets see what kind of links are in this page
    # remember in mechanize, unlike beautifulsoup, you can use the dot notation for page scrapping
    # link.url will get the url/href attr of the link, and link.text will get the raw text betweek the link tags
#for link in br.links():
#    print link.url + ' : ' + link.text


# lets say we want to go to the SQL Injection page
    # first we select the link by using the clink_link method, kind of like the select_form method
        # except it takes in an arg that could be url/href, or the text between the link tag
#new_link = br.click_link(text='SQL Injection')
    # then we go to the link by using the br.open() method
#br.open(new_link)

    #lets see where we are at
#printURL(br.geturl(), br.title())
