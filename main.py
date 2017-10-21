import os
import sys
import threading
import multiprocessing

bot_name = ['dudleybot','petuniabot']

def botexec(str):
    sys.stderr.write('I am '+str+ '\n')
    tmpstr='/opt/app/env/bin/python /opt/app/'+str+'.py'
    os.system(tmpstr)
    return

if __name__ == "__main__":
    jobs = []
    os.environ.setdefault('SLACK_BOT_TOKEN_DUDLEY', 'xoxb-256688870500-YufJlAqf7bnpNDWONBCkbsxh')
    os.environ.setdefault('SLACK_BOT_TOKEN_PETUNIA', 'xoxb-256652204482-32JtdYAv5f87VTALSr3FKgBA')
    for i in bot_name:
        p = multiprocessing.Process(target=botexec,args=(i,))
        jobs.append(p)
        p.start()
