#!/usr/bin/python

import os

fd = os.open(__file__, os.O_RDWR)

print 'file descriptor: ', fd

print 'closing file descriptor file'
os.close(fd)

print """
        hello,
        second line

"""
