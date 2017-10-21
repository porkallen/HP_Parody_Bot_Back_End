import os
import sys
import threading

threads = []
bot_name = ['dudleybot','petuniabot']
def botexec(str):
    sys.stdout.write('I am '+str+ '\n')
    sys.stderr.write('I am '+str+ '\n')
    tmpstr='/opt/app/env/bin/python /opt/app/'+str+'.py'
    os.system(tmpstr)
    return

if __name__ == "__main__":
    os.environ.setdefault('SLACK_BOT_TOKEN_DUDLEY', 'xoxb-256688870500-YufJlAqf7bnpNDWONBCkbsxh')
    os.environ.setdefault('SLACK_BOT_TOKEN_PETUNIA', 'xoxb-256652204482-32JtdYAv5f87VTALSr3FKgBA')
    for name in bot_name:
        t = threading.Thread(target=botexec(name))
        threads.append(t)
        t.start()