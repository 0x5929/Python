#!/usr/bin/python


# importing modules needed for simple http server

import SocketServer
import SimpleHTTPServer

# binding address to local host at port 80 for the server
address = ("0.0.0.0", 80)

print "Starting Server at 192.168.1.114:80...."

httpServer = SocketServer.TCPServer(address, SimpleHTTPServer.SimpleHTTPRequestHandler)

# allowing reusable address for quick rebinding
httpServer.allow_reuse_address = True

# starting the server
httpServer.serve_forever()
