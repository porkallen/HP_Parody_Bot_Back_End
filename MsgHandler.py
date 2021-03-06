#!/usr/bin/python           # This is server.py file
import os
import sys
import threading
import multiprocessing
import socket               # Import socket module
import SocketServer
from slackclient import SlackClient
from hp01.botMap import *
from hp01.procComm import *
from struct import *

#s = socket.socket()         # Create a socket object
#host = socket.gethostname() # Get local machine name
#port = 50000                # Reserve a port for your service.
HOST, BIND_PORT, PORT_RANGE = socket.gethostbyname(socket.gethostname()), 9999 , 50

class UserNode:
    ip = 0
    port = 0
    chapter = 0
    quiz = 0

#SocketServer server
class MsgHandler:
    threads = []
    procMsg = 0

    def childHandler(self,sock,ip,port):
        tmpBuf1 = ''
        tmpBuf2 = ''
        old_timeout = sock.gettimeout() # Save
        sock.settimeout(20) # Set time out
        try:
            data = sock.recv(1024)
            # do your stuff with socket
            sock.settimeout(old_timeout) # Restore
            tmpBuf1 += data
            sys.stderr.write('[*] Recv with IP:' + str(ip) + 'port:' + str(port)+'buf: '+tmpBuf1 +'\n')
            tmpBuf2, channel = self.procMsg.procMsgEx(tmpBuf1)
            sys.stderr.write('[*] Recv from process Successfully: '+ tmpBuf2 + '\n')
            sock.sendall(tmpBuf2+'\n')
            sock.close()
        except (socket.timeout, socket.gaierror) as error:
            sys.stderr.write('[*] Sock Recv Timeout')
        finally:
            sock.close()
        

        
    def msgHandler(self):
        try:
            #IPC communication
            self.procMsg = procComm(0,IS_MSG_HANDLER_PORT) 
            #Connect with Android
            msgSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            msgSock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            msgSock.bind((HOST, BIND_PORT))
            #msgSock.listen(10)
            sys.stderr.write("[*] Server listening on %s %d \n" %(HOST, BIND_PORT))
            msgSock.listen(100)
            while 1:
                (conn, (ip,port)) = msgSock.accept()
                sys.stderr.write('[*] Connected with IP:' + str(ip) + 'port:' + str(port)+'\n')
                t = threading.Thread(target = self.childHandler,args=(conn,ip,port))
                self.threads.append(t)
                t.start()
            msgSock.close()
        except KeyboardInterrupt as msg:
            sys.exit(0)
