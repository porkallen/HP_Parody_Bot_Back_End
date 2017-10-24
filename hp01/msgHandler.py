#!/usr/bin/python           # This is server.py file
import os
import sys
from threading import Thread
import multiprocessing
import socket               # Import socket module
import SocketServer
from slackclient import SlackClient


IS_SLACK= True
s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 50000                # Reserve a port for your service.

#SocketServer server
class msgHandl:
    server = 0
    IS_DATA = 0
    IS_CMD = 1
    def __init__(self,token):
        if(IS_SLACK == True):
            self.server = SlackClient(token)
        else:
            HOST, PORT = "localhost", 9999
            self.server = SocketServer.TCPServer((HOST, PORT), msgHandler)
            thread(target=server.serve_forever()).start()
        
    def msgConnect(self):
        if(IS_SLACK == True):
            return self.server.rtm_connect()
        else:
            return True
            
    def msgRecv(self):
        print('Msg Recv')
        if(IS_SLACK == True):
            return self.server.rtm_read()
        else:             
            # self.request is the TCP socket connected to the client
            server.data = self.server.request.recv(1024).strip()
            print('Server Says:')
            print "{} wrote:".format(server.client_address[0])
            print server.data
        
    def msgSend(self,channel,text,dataType):
        HOST, PORT = "localhost", 64300
        print('Msg Send')
        if(IS_SLACK == True):
            self.server.api_call("chat.postMessage", channel=channel,text=text, as_user=True)
        else:
            # Create a socket (SOCK_STREAM means a TCP socket)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Connect to server and send data
            sock.connect((HOST, PORT))
            sock.sendall(bytes(str + "\n"))
            sock.close()
            #print("Sent:     {}".format(data))
    
def MsgHandler(token):
    print('Msg init')
    obj = msgHandl(token)
    return obj
