#!/usr/bin/env python

'''
server.py comes paired with client.py to establish a simple send an receive a message serialized using json
'''

import socket
import simplejson as json

TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 1024  # Normally 1024, but we want fast response

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

conn, addr = s.accept()
print 'Connection address:', addr
while 1:
    data = conn.recv(BUFFER_SIZE)
    if not data: break
    print "received data: \n", data
    #print "decoded data: \n", json.loads(data)
    conn.send(data)  # echo
conn.close()
