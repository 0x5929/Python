#!/usr/bin/python


# this script will take my google chrome browser cookie for a website, and insert it to mechanize to test if successs

import mechanize

# creating the module
br = mechanize.Browser()

# creating cookie jar instance obj
cj = mechanize.CookieJar()

# creating cookie
    # a cookie has the following format: 
# Cookie(None, name, value, None, False, domain, True, False, path, True, False, None, False, None, None, None)
#cookie1 = mechanize.Cookie(0, 'security', 'low', None, False, 'http://192.168.1.81', True, False, '/', True, False, None, False, None, None, {}, False)

#cookie2 = mechanize.Cookie(0, 'PHPSESSID', 'm77lto4kcp4g0v4ce234kkt7cg', None, False, 'http://192.168.1.81', True, False, '/', True, False, None, False, None, None, {}, False)

br.set_simple_cookie(name='PHPSESSID', value='m77lto4kcp4g0v4ce234kkt7cg', domain='http://192.168.1.81', path='/DVWA')
br.set_simple_cookie(name='security', value='low', domain='http://192.168.1.81', path='/DVWA')

#print cookie1
#print "####"
#print cookie2

# setting such cookie in the cookiejar
#cj.set_cookie(cookie1)
#cj.set_cookie(cookie2)

#print "####"
#print cj
# having a browser set with the cookie jar

#br.set_cookiejar(cj)

# this is the test
br.open('http://localhost/DVWA')
print br.title()



