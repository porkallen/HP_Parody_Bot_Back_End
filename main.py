import os
import sys
import threading
import multiprocessing
from msgHandler import msgHandl

bot_name = ['msgHandler','dudleybot','petuniabot','bob_hair_cut','hogford']
#bot_name = ['msgHandler','dudleybot']

def botexec(str):
    if(str == 'msgHandler'):
        msgServ.MsgHandler()
    else:
        sys.stderr.write('I am '+str+ '\n')
        loc = os.path.abspath('.')
        tmpstr=loc+'/env/bin/python '+loc+'/hp01/'+str+'.py'
        print(tmpstr)
        os.system(tmpstr)
    return

if __name__ == "__main__":
    msgServ = msgHandl();
    jobs = []
    loc = os.path.abspath('.')
    os.environ.setdefault('SLACK_BOT_TOKEN_DUDLEY', 'xoxb-256688870500-YufJlAqf7bnpNDWONBCkbsxh')
    os.environ.setdefault('SLACK_BOT_TOKEN_PETUNIA', 'xoxb-256652204482-32JtdYAv5f87VTALSr3FKgBA')
    os.environ.setdefault('SLACK_BOT_TOKEN_BOB', 'xoxb-260225956352-zGKN4Tfw2iQ8Rn97HwROAIY0')
    os.environ.setdefault('SLACK_BOT_TOKEN_HOGFORD', 'xoxb-260347880417-cykm48o6jvV2Zu604TTVTG3h')
    os.environ.setdefault('BOT_ID_PETUNIA', 'U7JK660E6')
    os.environ.setdefault('BOT_ID_DUDLEY', 'U7JL8RLEQ')
    os.environ.setdefault('BOT_ID_BOB_HAIR_CUT', 'U7N6MU4AC')
    os.environ.setdefault('BOT_ID_HOGFORD', 'U7NA7RWC9')
    for i in bot_name:
        p = multiprocessing.Process(target=botexec,args=(i,))
        jobs.append(p)
        p.start()