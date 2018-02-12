#!/usr/bin/python

import mechanize
import urllib
from bs4 import BeautifulSoup


#br = mechanize.Browser()
#br.open("http://www.duckduckgo.com")
#html = br.response().read()
#bs = BeautifulSoup(html, 'lxml')
#print bs.prettify()
#print "="*100
#print html

def f (args):
    if not args[2]:
        print "the third arg is missing from tuple but no error exception"
    else:
        print 'we are okay, all arugs passed in'

f((1,2, None))

