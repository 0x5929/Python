#!/usr/bin/python


# to import the mechanize module
	# it is used to emulate browser, and do inspections on documents
	# more importantly its used to fill in form data and submit forms
import mechanize


# we can create a browser obj
b = mechanize.Browser()

# we can open an url, and its html response
b.open('http://www.securitytube.net/video/3000')

# we can find all the forms in the http page
	# by using the forms() method to dump all the http forms
for form in b.forms():
	print "THIS IS THE FORM IN THE WEBPAGE: \n",  form


# so what we want to do is to fill out data in the form, 
# and send it to the destination and parse the response
	# using the mechanize browser object, we can select the element that we are interested to fill in 
	# using the select_form method and passing in 0 for nr argument for the first form. 	

b.select_form(nr=0)

# NOW ALL ACTIVITIES ARE IN THE SELECTED FORM'S CONTEXT	
	# now in order to select and set the 'q' form/textinput
	# we are already in the selected form's context so 
	# b.form is the form we selected
	# we are choosing the 'q' form field, and we can access it with the [] notation, not dot
b.form['q'] = 'searched string'

# now we can submit the form by using the submit method
	# and we are printing its response
response = b.submit()
print "THIS IS THE RESPONSE: \n", response

# we could also find the links in a page on the emulated browser
	# mechanize unlike beautiful soup, we are not looking for tags
	# it is putting all form in the return list of forms() method
	# and so are the links in the return list of links() method
			# NOTE: REMEMBER THAT IN THE LINK, if we wanted to get the attributes, we have to use the dot notation
			# such as link.url, or link.text, not link['url'] wont work	
for link in b.links():
#	print "LINK in document: \n", link 
	print link.url + " : " + link.text









