#!/usr/bin/python


# mutli thread socket server

import socket
import threading


# threading class

class SlaveThreads(threading.Thread):
	def __init__(self, client, clientIP, clientPORT): # think about what each thread will recieve as args
		threading.Thread.__init__(self)	#calling parent thread class for thread workers
		self.client = client
		self.clientIP = clientIP
		self.clientPORT = clientPORT
	def run(self):
		data = 'dummy'
		while data: # this will keep running until connection is closed
			data = client.recv(6000)
			print "Client Sent: ", data
			client.send(data)
		else:
			print "Closing Client Connection...."
			client.close() 
			print "Closing Server Connection...."
			tcpSocket.close()	
		
# starting up the tcp socket server

tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpSocket.bind(("0.0.0.0", 8000))
print "Server listening on 192.168.1.114:8000"
tcpSocket.listen(5)

for i in range(5):
	print "Waiting for a client to connect~~~"
	(client, (ip, port)) = tcpSocket.accept()
	print "Starting to Create Slave Number %" %i
	newSlave = SaveThreads(client, ip, port)
	newSlave.start()





