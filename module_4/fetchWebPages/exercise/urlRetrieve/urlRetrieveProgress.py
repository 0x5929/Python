#!/usr/bin/python



# importing modules

import urllib

# i want to download a pdf

# setting up the constant variables
url = 'http://www.st-inst.com/pdf/School_Catalog.pdf?osCAdminID=db79d23bfb6eeee402ab7f078fee816c&osCAdminID=24495974356bfbcbeeb9ddafa3a0ac99'
base_url = 'http://www.st-inst.com/pdf/School_Catalog.pdf'

args = {
	'osCAdminID': 'db79d23bfb6eeee402ab7f078fee816c',
	'osCAdminID': '24495974356bfbcbeeb9ddafa3a0ac99'
}

encoded_args = urllib.urlencode(args)

location_to_save = '/home/kevin/Python/module_4/fetchWebPages/exercise/urlRetrieve/school_catalog.pdf'

# defining the progresshandler function

def progressHandler(block_count, block_size, total_size):
	downloaded = int(block_count * block_size)
	still_need_to_download = int(total_size - (block_count*block_size))
	percentage = int((block_count * block_size * 100) / total_size)
	print "*"* 100
	print "THIS IS THE PROGRESS PERCENTAGE: ", percentage
	print "We have downloaded:  " + str(downloaded) + " bytes"
	print "We still need to download:  " + str(still_need_to_download) + " bytes"	
	print "*" * 100

# the first arg is the url to download, second arg is the local location to save to, 
# third arg is a call back function everytime a block is read/downloaded
urllib.urlretrieve(base_url + '?' + encoded_args, location_to_save, reporthook=progressHandler)


