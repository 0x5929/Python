#!/usr/bin/python


# this script will be our path helper
# changing the default module look up path in sys.path[0]
# to the directories we need to test

import os
import sys


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


import server
from resources import * 



