#!/usr/bin/python

import mechanize
import urllib
from bs4 import BeautifulSoup


br = mechanize.Browser()
br.open("http://www.duckduckgo.com")
html = br.response().read()
bs = BeautifulSoup(html, 'lxml')
print bs.prettify()
print "="*100
print html
