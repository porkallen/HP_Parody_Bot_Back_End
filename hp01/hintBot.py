import os
import time
from procComm import *
from botMap import *


def send_hint(milestone_marker):
    #
    # Message to @GP:
    # The strcuture of hint dictionary is
    # key: milestone, value: 3 hints
    # Each time users request hint, it will send back the hint to current milestone.
    #
    hint_set = {
        0: ['Nothing', 'Nothing', 'Nothing'],
        1: ['You should probably respond to Aunt Petunia', 'You should probably tell Petunia you are going to do it',
            'Type: YES'],
        2: ['You should probably ask Aunt Petunia about the text', 'Ask Aunt Petunia',
            'Type: @AuntPetunia What is this letter from Hogford about?'],
        3: ['Feel free to insult Dudley', 'Feel free to attack Dudley with Magic',
            'You can also threaten Dudley with Magic']
    }
    return hint_set[milestone_marker]

hintBot = procMsgInit(0, IS_HINT_BOT_PORT)

if __name__ == "__main__":

    READ_WEBSOCKET_DELAY = 1  # 1 second delay between reading from firehose
    if hintBot.procMsgConn():
        print("Hint Bot connected and running!")
        while True:
            command, channel, tmp_marker = parse_slack_output(
                hintBot.procMsgRecv())
            if command and channel:
                milestone_marker = handle_command(
                    command, channel, milestone_marker)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
