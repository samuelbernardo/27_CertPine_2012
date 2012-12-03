#!/usr/bin/env python

import socket
import simplejson as json

'''
client.py comes paired with server.py to establish a simple send an receive a message serialized using json
'''

TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 1024
MESSAGE = [ { 'a':'A', 'b':(2, 4), 'c':3.0 } ]

#MESSAGE = packet.Packet('www.bpinet.pt', 144082741558875710455667109925152810750, before, after);

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.send(json.dumps(MESSAGE))
data = s.recv(BUFFER_SIZE)
s.close()
print "received data: \n", data
print "decoded data: \n", json.loads(data)

