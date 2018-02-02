#!/usr/bin/python

# this script will automate the process of logging on to gmail.com 


# import important modules
import sys  # for exiting the system
import time # to sleep the system while in virtual browser view, so it stays on before shutting down
import getpass  # for password hashing
from pyvirtualdisplay import Display    #for selelnium to display browser in a linux system
from selenium import webdriver          # selenium webdriver browser obj
from selenium.webdriver.common.keys import Keys # this will import key functions like Enter or Esc, Tab...etc
from selenium.webdriver.common.by import By # this will give further filters for certain locate element functions
from selenium.webdriver.support.ui import WebDriverWait # this will sleep the selenium script and waits for execution until a condition
from selenium.webdriver.support import expected_conditions as EC    # this will be the codition for wait to execute script

# greetings
print "[!] Welcome to your virtual gmail sign in using selenium"

# grabbing user input
try: 
    email_username = raw_input("[!] Please enter your gmail email: ")
    email_password = getpass.getpass("[!] Please enter your gmail password: ")
    seconds_to_stay_on = float(raw_input("[!] Please enter the amount of seconds we want the virtual browser to stay open after logging in: "))
except KeyboardInterrupt:
    print "[!] User requested shutdown"
    print "[!] Shutting down"
    sys.exit(1)

# starting out the display, needed for linux users
Xephyr = Display(visible=1, size=(800, 800))
Xephyr.start()
    # there are two types, Xvfb or Xephyr
        # Xvfb, is a virtual one, and there is no output 
        #  Xephyr is the one that we can have output on a virtual screen

br = webdriver.Chrome()

# lets connect to gmail using the get method, same as open method in mechanize browser
br.get("http://www.gmail.com")

try: 
    assert "Gmail" in br.title
except: 
    print '[!] Error: cannot connect to gmail.com! Exiting the system...'
    br.quit()
    Xephyr.stop()
    sys.exit(1)

try: 
    # lets put in the email now
    element = br.find_element_by_name('identifier')
    element.clear()     # clearing if any preexisting fields
    element.send_keys(email_username)
    element.send_keys(Keys.RETURN)  # the return carriage 
except: 
    print "[!] Error: gmail email username is incorrect! Exiting the system..."
    br.quit()
    Xephyr.stop()
    sys.exit(1)

# lets put in the password, reusing the element var because we are at a new page now
# we need to wait until ajax/angularjs shows password input first
    # we will use the webdriverwait obj with the browser driver to be the instance we want it to wait, and the second arg 
    # is the amount of time in seconds we want to wait, which is 5, then we will use the until method to set a condition
    # using the expectedCondition obj, and its presenceOfElementLocation method, which takes a filter condition
    # this presence method takes a tuple, first element is the type, which is by name, 
    # then second element of that, which is the value:  password
try: 
    element = WebDriverWait(br, 5).until(EC.presence_of_element_located((By.NAME, "password")))
    element.clear()
    element.send_keys(email_password)
    element.send_keys(Keys.RETURN)
    time.sleep(seconds_to_stay_on)
except KeyboardInterrupt:    
    print "[!] Use requested shutdown!"
    print "[!] Shutting down..."
    br.quit()
    Xephyr.stop()
    sys.exit(1)
finally:
    print "[!] The system had completed its tasks"
    print "[!] Shutting down..."
    br.quit()
    Xephyr.stop()
    sys.exit(0)


