#!/usr/bin/python           # This is server.py file
import os
import sys
from threading import Thread
import multiprocessing
import socket               # Import socket module
from slackclient import SlackClient
from botMap import *


IS_SLACK= False

 #
 #   Data Format:
 # 0: <Msg Type>
 # 1: <Port>
 #   2: <Chapter>
 #   3: <MileStone>
 # 4: <Text MSg>

class BotMsgNode:
    msgType = 0
    msgTo = 0
    chapter = 0
    milestone = 0
    msg = ''
    BOT_MSG_TYPE_TXT = 0
    BOT_MSG_TYPE_HINT = 1  
    BOT_MSG_IDX_MSG = 0
    BOT_MSG_IDX_MSG_TYPE = 1
    BOT_MSG_IDX_MSGTO = 2
    BOT_MSG_IDX_CHAP = 3
    BOT_MSG_IDX_MS = 4
    SPLIT_CHAR = '!@#'
    def formatBotMsg(self,msg,msgType,msgTo,chapter,milestone):
        strPool = [str(msg),str(msgType),str(msgTo),str(chapter),str(milestone)]
        retStr = ''
        for i in range(len(strPool) - 1):
            retStr += strPool[i]+self.SPLIT_CHAR
        retStr += strPool[len(strPool)-1]
        print("format: "+retStr);
        return retStr

    def parseBotMsg(self,msg):
        # return msgType,Port.milestron,msg
        strPool = []
        strPool = msg.split(self.SPLIT_CHAR);
        return strPool[self.BOT_MSG_IDX_MSG],strPool[self.BOT_MSG_IDX_MSG_TYPE],strPool[self.BOT_MSG_IDX_MSGTO],strPool[self.BOT_MSG_IDX_CHAP],strPool[self.BOT_MSG_IDX_MS]

#s = socket.socket()         # Create a socket object
#host = socket.gethostname() # Get local machine name
#port = 50000                # Reserve a port for your service.
#SocketServer server
class procComm:
    HOST = socket.gethostbyname(socket.gethostname())
    port = 0
    server = 0
    IS_DATA = 0
    IS_CMD = 1
    def __init__(self,token,port):
        if(IS_SLACK == True):
            self.server = SlackClient(token)
        else:
            self.port = port
            self.server = socket.socket(socket.AF_INET,socket.SOCK_DGRAM, socket.IPPROTO_UDP)
            self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server.bind((self.HOST,  self.port))
            sys.stderr.write('Msg Bind: '+str(self.port)+'\n')

    def procMsgEx(self,data):
        botmsg = BotMsgNode();
        for AT_BOT in BOT_MSG_HEAD:
            if data.startswith(AT_BOT):
                sys.stderr.write('[*] msgEx:'+str(BOT_MAP[AT_BOT][0]))
                msg, msgType, port, chapter, milestone = botmsg.parseBotMsg(data)
                self.procMsgSend(
                    channel = BOT_MAP[AT_BOT][0],text = msg,
                    chapter = 0,milestone = 0,
                    dataType = msgType
                )
                ret = self.procMsgRecv()
                retStr = botmsg.formatBotMsg(
                    msg = ret[0]['text'],msgTo = ret[0]['channel'],
                    msgType = ret[1]['type'],chapter = ret[1]['chapter'],
                    milestone = ret[1]['MS']
                )
                ret[0]['channel'] = BOT_MAP[AT_BOT][0]
                return retStr,ret[0]['channel']
        return '',0
        
    def procMsgConn(self):
        if(IS_SLACK == True):
            return self.server.rtm_connect()
        else:
            return True
            
    def procMsgRecv(self):
        #print('Msg Recv')
        botmsg = BotMsgNode();
        if(IS_SLACK == True):
            return self.server.rtm_read()
        else:           
            output_list = []
            strPool = []
            # self.request is the UDP socket connected to the client
             #   Data Format:
            data = self.server.recv(1024).strip()
            strPool = botmsg.parseBotMsg(data)
            sys.stderr.write('[*] procMsgRecv '+str(self.server.getsockname())+' data: '+data +'\n')
            output_list.append({'text':strPool[botmsg.BOT_MSG_IDX_MSG],'channel':strPool[botmsg.BOT_MSG_IDX_MSGTO]})
            output_list.append({'type':strPool[botmsg.BOT_MSG_IDX_MSG_TYPE],'chapter':strPool[botmsg.BOT_MSG_IDX_CHAP], 'MS':strPool[botmsg.BOT_MSG_IDX_MS]})
            #output_list.append({'type':strPool[botmsg.BOT_MSG_IDX_MSG_TYPE],'chapter':strPool[botmsg.BOT_MSG_IDX_CHAP]})
            #output_list.append({'MS':strPool[botmsg.BOT_MSG_IDX_MS]})
            return output_list
        
    def procMsgSend(self,channel,text,chapter,milestone,dataType):
        port = channel
        botmsg = BotMsgNode();
        if(IS_SLACK == True):
            if(dataType == botmsg.BOT_MSG_TYPE_TXT):
                self.server.api_call("chat.postMessage", channel=channel,text=text, as_user=True)
        else:
            msgTx = botmsg.formatBotMsg(text,dataType,channel,chapter,milestone)
            sys.stderr.write('[*]procMsgSend '+str(self.server.getsockname())+ ' to ' + str(port)+'\n')
            server_address = (self.HOST, port)
            self.server.sendto(bytes(msgTx + '\n'),server_address)
            #print("Sent:     {}".format(data))
    
def procMsgInit(token,port):
    sys.stderr.write('Msg init\n')
    obj = procComm(token,port)
    return obj
