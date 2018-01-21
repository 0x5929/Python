#!/usr/bin/python



# this script is to get comforatble with fetching data/webpages using the 
# urllib and urllib2 library/modules

import urllib

# to fetch data from a web page, we can just use the urlopen method from urllib as such
	# the arg is any web url
httpResponse = urllib.urlopen("http://localhost")

# we should analyze the response code the server sends back to us
	# 200 -> ok
	# 404 -> not found
if httpResponse.code == 200:
	print "reponse code is 200, everything is okay"
else: 
	print "response code is not 200, something is wrong"

# there are two parts in every http resposne: 
	# first part is the http header, includes cookies, code, date, etc..
	# second part is the data, html page which the server returns

# in order to access the second part, we can just do urllib.urlopen("www.google.com").read()
	# it would output the html data
print "\nPrinting the HTML response: \n"
print httpResponse.read()

# remember in python we can use the build in method to use on objects to see all the methods it contains
	# by using dir(httpResponse), for direction i suppose

# to return header values, we can just use the items method on the headers method of the response
listOfHeaderValues = httpResponse.headers.items()
print "list of header keys and values in tuple form: \n", listOfHeaderValues


print "*"*50 + " AND BELOW IS A BETTER VERSION FOR READABILITY " + "*"*50
for header, value in listOfHeaderValues: 
	print header + ' : ' + value
print "*"*100



# if we wanted a more complex url with parameters in the get request such as 

url = "http://www.securitytube.net/groups?operation=view&groupId=10"

# where the base url is

base_url = "http://www.securitytube.net/groups"

# to safely parse the url with all the params
	# we need to create a dictionary with all the key and values of the parameters

args = {
	'operation' : 'view',
	'groupId'   : 10
}
# then we would need to encode the args into the url by using the urlencode method of urllib, and give it the arguments
encoded_args = urllib.urlencode(args)

# then in order to fetch data with the url that has encoded args we use the same url open method of urllib like such 
response = urllib.urlopen(base_url + "?" + encoded_args)

if response.code == 200:
	print "security tube encoded url fetch is 200 a-ok"
	print "*"*50 + " THERE ARE THE HTML CONTENT " + "*"*50
	print response.read()
	print "*"*100
else:
	print "something went wrong with fetching securitytube with encoded url"



## NOTE: by default urlopen is a get request, if you wanted to do a post request with the encoded arguments, pass 
	# the encoded args in a seperate argument like: a = urllib.urlopen(base_url, encoded_args)
	# however, some url sites wont allow post request if it was only meant to do get requests instead











