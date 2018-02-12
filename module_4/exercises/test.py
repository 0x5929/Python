#!/usr/bin/python

import mechanize
import urllib
from bs4 import BeautifulSoup
import threading

threads = []

def anotherOne(browserInstance):
#    print browserInstance.geturl()
    pass
def main():
#    br = mechanize.Browser()
 #   br.open("http://www.duckduckgo.com")
  #  anotherOne(br)
    for i in range(1,11):
        t = threading.Thread(target=anotherOne, args=(i,))
        threads.append(t)
    print threads

main()
