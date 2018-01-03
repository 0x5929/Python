#!/usr/bin/python

from ftplib import FTP

ftp = FTP('ftp.debian.org')
ftp.login()
ftp.cwd('/')
ftp.retrlines('LIST')
ftp.quit()






