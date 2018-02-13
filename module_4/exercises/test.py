#!/usr/bin/python

import mechanize
import urllib
from bs4 import BeautifulSoup
import threading

#threads = []

#def anotherOne(browserInstance):
##    print browserInstance.geturl()
#    pass
#def main():
##    br = mechanize.Browser()
# #   br.open("http://www.duckduckgo.com")
#  #  anotherOne(br)
#    for i in range(1,11):
#        t = threading.Thread(target=anotherOne, args=(i,))
#        threads.append(t)
#    print threads
#
##br = mechanize.Browser()
##br.open("http://www.duckduckgo.com")
##html = br.response().read()
##bs = BeautifulSoup(html, 'lxml')
##print bs.prettify()
##print "="*100
##print html
#
#def f (args):
#    if not args[2]:
#        print "the third arg is missing from tuple but no error exception"
#    else:
#        print 'we are okay, all arugs passed in'
#
#f((1,2, None))
#
