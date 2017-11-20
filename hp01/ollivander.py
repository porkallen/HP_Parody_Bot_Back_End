import os
import time
from utils import wit_response, wit_ollivander_response
from procComm import *
from botMap import *
from chapter_02_script import *



#random
READ_DELAY = 2


def send_hint(milestone_marker):
    #
    # Message to @GP:
    # The strcuture of hint dictionary is
    # key: milestone, value: 3 hints
    # Each time users request hint, it will send back the hint to current milestone.
    #
    hint_set = {
        0:['Type: "Spin Wand" (no quotes). you will need to use the hints for this section'],
        1:['Type: "Twirl Wand"'],
        2:['Type: "Wave Wand"'],
    }
    return hint_set[milestone_marker]


def handle_command(command, channel, milestone_marker):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """
    response = "Well if it is not Mr. Potter"

    if command.startswith(AT_OLLIVANDER):

        check = False
        general_text = command.split(AT_OLLIVANDER)[1].strip().lower()

        ##########################################################################
        #                                                                        #
        #  BLOCKS NEED TO BE IN REVERSE ORDER SO MILESTONES DON'T GET OVERRIDEN  #
        #                                                                        #
        ##########################################################################

        ##############################################
        #                  BLOCK 3                   #
        # This is what the bot intialize says        #
        ##############################################
        if general_text == "wave wand":
            response = CH02_ollivander_REPLY_03
            time.sleep(READ_DELAY)
            check = True
            #HAGRID IS TRIGGERED HERE
            milestone_marker = 6

        ##############################################
        #                  BLOCK 2                   #
        # This is what the bot intialize says        #
        ##############################################
        if general_text == "twirl wand":
            response = CH02_ollivander_REPLY_02
            time.sleep(READ_DELAY)
            check = True
            milestone_marker = 5

        ##############################################
        #                  BLOCK 1                   #
        # First spell attempted                      #
        ##############################################
        if general_text == "spin wand":
            response = CH02_ollivander_REPLY_01
            time.sleep(READ_DELAY)
            check = True
            milestone_marker = 4



        ##############################################
        #                  BLOCK 0                   #
        # This is what the bot intialize says        #
        ##############################################
        if general_text == START_COMMAND_OLLIVANDER:
            response = CH02_ollivander_STATEMENT_01
            time.sleep(READ_DELAY)
            check = True
            milestone_marker = 3

        '''''
        #################################################
        #                  BLOCK 2                      #
        # This is the banter between Bots post hair cut #
        #################################################
        if milestone_marker == 3:

            if general_text == RESPONSE_3:
                response = STATEMENT_06
                time.sleep(READ_DELAY)
                check = True
                # @Doby this is the end of Chapter 1. The next cut scene will play from here.


        '''
        ##########
        # WIT.AI #
        ##########
        if not check:

            response_wit_parsed = wit_ollivander_response(general_text)

            response = "Well someone should really train the Wit bot"

            print(response_wit_parsed)


            '''''
            #First checking to see if Wit picked up an intent
            if 'intent' in response_wit_parsed:
                ##########################################################################
                #                                                                        #
                #  BLOCKS NEED TO BE IN REVERSE ORDER SO MILESTONES DON'T GET OVERRIDEN  #
                #                                                                        #
                ##########################################################################

                ###################################################
                #                  BLOCK 3                        #
                # Getting to Woz                                  #
                ###################################################
                if response_wit_parsed['intent'] == ['affirmative'] and milestone_marker == 2:
                    response = CH02_ollivander_REPLY_03_Positive
                    time.sleep(READ_DELAY)

                if response_wit_parsed['intent'] == ['question_wozniak'] and milestone_marker == 2:
                    response = CH02_ollivander_REPLY_03_Woz
                    time.sleep(READ_DELAY)
                    milestone_marker = 3

                ## NEED TO HANDLE IF THEY SAY NO?

                ###################################################
                #                  BLOCK 2                        #
                # Either telling more or skipping to Gringots     #
                ###################################################
                if response_wit_parsed['intent'] == ['affirmative'] and milestone_marker == 1:
                    response = CH02_ollivander_REPLY_02_Positive
                    time.sleep(READ_DELAY)
                    milestone_marker = 2

                elif response_wit_parsed['intent'] == ['negative'] and milestone_marker == 1:
                    response = CH02_ollivander_REPLY_02_Negative
                    time.sleep(READ_DELAY)
                    milestone_marker = 2

                ##############################################
                #                  BLOCK 1                   #
                # Telling User about the basics              #
                ##############################################
                print(milestone_marker)
                if response_wit_parsed['intent'] == ['affirmative'] and milestone_marker == 0:
                    response = CH02_ollivander_REPLY_01_Postive
                    time.sleep(READ_DELAY)
                    milestone_marker = 1


                elif response_wit_parsed['intent'] == ['negative'] and milestone_marker == 0:
                    response = CH02_ollivander_REPLY_01_Negative
                    time.sleep(READ_DELAY)
                    milestone_marker = 1

                ##############################################
                #                  BLOCK X                   #
                # This Block is to catch RANDOM phrases      #
                ##############################################
                if 'wit/greetings' in response_wit_parsed:
                    if response_wit_parsed['wit/greetings'] == ['true']:
                        response = "HAHAHA hello ther' Mr. Potter!"
                        time.sleep(READ_DELAY)

            else:
                response = "Hhmmmm seems like I didn' quite make that out ther'..."
                time.sleep(READ_DELAY)
            '''


    slack_client_ollivander.procMsgSend(
        channel=IS_MSG_HANDLER_PORT,
        text=response,
        chapter=1,
        milestone=milestone_marker,
        dataType=slack_client_ollivander.IS_DATA,
        msgFrom=IS_OLLIVANDER_PORT
    )
    return milestone_marker


def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    ret1 = None
    ret2 = None
    ret3 = None
    msgFrom = None
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_OLLIVANDER in output['text']:
                # return text after the @ mention, whitespace removed
                # return output['text'].split(AT_BOT)[1].strip().lower(),
                ret1 = output['text']
                ret2 = output['channel']
            if output and 'msgFrom' in output and output['msgFrom']:
                msgFrom = output['msgFrom']
            if output and 'MS' in output and output['MS']:
                ret3 = output['MS']
    if int(msgFrom) != IS_MSG_HANDLER_PORT:
        ret3 = None
    return ret1,ret2,ret3


# instantiate Slack & Twilio clients
slack_client_ollivander = procMsgInit(os.environ.get('SLACK_BOT_TOKEN_OLLIVANDER'),IS_OLLIVANDER_PORT)

if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    ##### Progression tracking #############
    milestone_marker = 3
    tmp_marker = None
    ########################################
    if slack_client_ollivander.procMsgConn():
        print("Ollivander Bot connected and running!")
        while True:
            
            command, channel, tmp_marker = parse_slack_output(
                slack_client_ollivander.procMsgRecv())
            if tmp_marker:
                milestone_marker = int(tmp_marker)
            if command and channel:
                milestone_marker = handle_command(command, channel, milestone_marker)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
