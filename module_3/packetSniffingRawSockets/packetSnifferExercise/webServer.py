#!/usr/bin/python


import SocketServer
import SimpleHTTPServer


httpServer = SocketServer.TCPServer(("", 80), SimpleHTTPServer.SimpleHTTPRequestHandler)

print "HTTP Server starting on localhost: 192.168.1.114:80"

httpServer.serve_forever()



