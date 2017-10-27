import os
import sys
import threading
import multiprocessing
from msgHandler import msgHandl

bot_name = ['msgHandler','dudleybot','petuniabot']
#bot_name = ['msgHandler','dudleybot']

def botexec(str):
    if(str == 'msgHandler'):
        msgServ.MsgHandler()
    else:
        sys.stderr.write('I am '+str+ '\n')
        loc = os.path.abspath('.')
        tmpstr=loc+'env/bin/python '+loc+'hp01/'+str+'.py'
        print(tmpstr)
        os.system(tmpstr)
    return

if __name__ == "__main__":
    msgServ = msgHandl();
    jobs = []
    loc = os.path.abspath('.')
    os.environ.setdefault('SLACK_BOT_TOKEN_DUDLEY', 'xoxb-256688870500-YufJlAqf7bnpNDWONBCkbsxh')
    os.environ.setdefault('SLACK_BOT_TOKEN_PETUNIA', 'xoxb-256652204482-32JtdYAv5f87VTALSr3FKgBA')
    os.environ.setdefault('BOT_ID_PETUNIA', 'U7JK660E6')
    os.environ.setdefault('BOT_ID_DUDLEY', 'U7JL8RLEQ')
    for i in bot_name:
        p = multiprocessing.Process(target=botexec,args=(i,))
        jobs.append(p)
        p.start()