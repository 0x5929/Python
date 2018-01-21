#!/usr/bin/python



# this script is using the beautiful soup third party lib to parse html
	# version 4 and onwards allows use of lxml and html5lib as parser engine, we will use lxml
		# it also handles bad html and encoding very well

# importing modules

from bs4 import BeautifulSoup
import urllib

# first lets fetch a webpage for its html content
url = "http://www.st-inst.com/information.php?info_id=1&osCsid=hpplco2p910ugkdf1l5ih74l46"
html = urllib.urlopen(url)

if html.code == 200:
	print "*"*100
	print "code is 200, and everything is okay"
	print "*"* 100
else: 
	print "html.code is not 200, something is wrong"
	print html.code
# lets put the html into beautiful soup
	# first arg is the html content
	# second arg is the parser, we dont want the default, b/c its bad
parsed = BeautifulSoup(html.read(), "lxml")

print "*"*100
print "HTML CONTENT BY BEAUTIFUL SOUP"
print parsed
print "*"*100

	# to view the title's string value of the html, we used parsed.title.string
print "TITLE STRING: ", parsed.title.string

	# we want to find all of meta tags, because the above method only returns the first one
	# we can use parsed.find_all method, with arg of the tag name, returns a list
allMetaTags = parsed.find_all("meta")
print "list of meta tags: ", allMetaTags


allLinkTags = parsed.find_all("a")
for element in allLinkTags:
#	print "element: ", element
#	print element.href	# or print element['href']
	print element['href']	# in python, we need to access dictionary, lists, and tuples with [] notation, dictionarys can take key in ''
	
# in order to extract all the text in a html document, including comments, beautifulsoup makes it easy, by the get_text() method
allText = parsed.get_text()

print "*"*300
print 'ALL TEXT FROM HTML'
print allText
print "*"*300



































