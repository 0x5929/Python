#!/usr/bin/python


# simple httpserver
# done with socketServer framework
import SocketServer
import SimpleHTTPServer

# NOTE: SimpleHTTPServer is a subclass of -> BaseHTTPServer which is a subclass of  -> SocketServer.TCPServer
# so the SimppleHTTPRequestHandler can overide its parent or grandparent method of BasicRequestHandler method

class HttpRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
	# this handler is overwritten so wheneever a get request comes to the server, below code will be
	# executed
	def do_GET(self):
	# so if the url is /admin, we execute the following, and write:
	# also we are writing the request headers as well
		if self.path == '/admin':
			self.wfile.write("This page is only for Admins!!!")
			self.wfile.write(self.headers)
		else: # for all other requests or url, we do the default get handler, which is to list all pages
			SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)





address = ("0.0.0.0", 10000)

httpServer = SocketServer.TCPServer(address, HttpRequestHandler)
httpServer.allow_reuse_address = True

print "Are we allowing resuable address? ", httpServer.allow_reuse_address
# By default, we can just use the default SimpleHTTPServer.SimpleHTTPRequestHandler as the handler
# this will list out the current directory of the file if we check it out on the browser with ip and port

#httpServer = SocketServer.TCPServer(address, SimpleHTTPServer.SimpleHTTPRequestHandler)

httpServer.serve_forever()
