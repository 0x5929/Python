#!/usr/bin/python

import mechanize
import urllib
from bs4 import BeautifulSoup
import threading
import argparse


p = argparse.ArgumentParser(description='THIS IS A TEST PROGRAM')
p.add_argument('first',  nargs='?' ,type=int, help='this is the first string to be printed')
p.add_argument('second', nargs='?', type=str, help='this is the second string to be printed')
a = p.parse_args()

print a.first
print a.second
















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
