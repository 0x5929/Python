#!/usr/bin/python


	# screen scrapper
	# we need to write a program that can fetch html from a webpage, parse it and find interesting info from it

	#  very html structure dependent. minor changes might break the scrapper

# importing the modules

import urllib
from bs4 import BeautifulSoup

response = urllib.urlopen("http://www.securitytube.net/video/3000")


html = response.read()

# parsing the html with beautiful soup

bs = BeautifulSoup(html, 'lxml')

# the find method can also take an attribute as input, if there are no children tags or elements you want to mention in the find
description = bs.find('div', id='description') 
# note for this document, we couldnt find a link for description
print "THIS IS THE DESCRIPTION PART OF THE VIDEO: \n", description

# the find method can take a tag name as an arg, with a following arg as a dictionary with key value of its children
	# in this case title tag and its property are its children key and value pair
videoLink = bs.find("iframe", {'title': 'YouTube video player'})

print 'HERE ARE THE VIDEO LINK LOOKED FOR USING FIND IFRAME TAG AND ITS CHILDREN IN A DICTIONARY: \n', videoLink
print '*'*100
print "Video's Source link : ", videoLink['src']
# we cannot find src in the video link either

# finding forms

forms = bs.find_all('form')


print forms
