import os
import time
from utils import wit_response, wit_hagrid_response
from procComm import *
from botMap import *
from chapter_02_script import *



#random
READ_DELAY = 2

def send_hint():
    #
    # Message to @GP:
    # The strcuture of hint dictionary is
    # key: milestone, value: 3 hints
    # Each time users request hint, it will send back the hint to current milestone.
    #
    hint_set = {
        0:['Respond Yes or No','Type: Yes or Type: No'],
        1:['Respond Yes or No','Type: Yes or Type: No'],
        2:['Respond Yes to keep going','Type: Yes'],
        3: ['Ask about Wozniak', 'Type: Who is Professor Wozniak'],
    }
    return hint_set[milestone_marker]


def handle_command(command, channel, milestone_marker):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """
    response = "Hello Gary, gurd to see ya"

    if command.startswith(AT_HAGRID):

        check = False
        general_text = command.split(AT_HAGRID)[1].strip().lower()

        #ENTRY BLOCK OF CODE NO MILSETONE CHECK NEEDED

        # @Doby, I seperated this into Non Wit and Wit section... but I think it needs to be organized better.
        # @Doby, The flow is a bit odd because I go back and forth. Look at Block 2 for example.

        ##############################################
        #                  BLOCK 0                   #
        # This is what the bot intialize says        #
        ##############################################
        if general_text == START_COMMAND:
            response = CH02_hagrid_STATEMENT_01
            time.sleep(READ_DELAY)
            check = True
            milestone_marker = 0

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

            response_wit_parsed = wit_hagrid_response(general_text)

            response = "Well err, what ya want to know? Just say yes if you want to keep going"

            print(response_wit_parsed)

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
                    response = CH02_hagrid_REPLY_03_Positive
                    time.sleep(READ_DELAY)

                if response_wit_parsed['intent'] == ['question_wozniak'] and milestone_marker == 2:
                    response = CH02_hagrid_REPLY_03_Woz
                    time.sleep(READ_DELAY)
                    milestone_marker = 3

                ## NEED TO HANDLE IF THEY SAY NO?

                ###################################################
                #                  BLOCK 2                        #
                # Either telling more or skipping to Gringots     #
                ###################################################
                if response_wit_parsed['intent'] == ['affirmative'] and milestone_marker == 1:
                    response = CH02_hagrid_REPLY_02_Positive
                    time.sleep(READ_DELAY)
                    milestone_marker = 2

                elif response_wit_parsed['intent'] == ['negative'] and milestone_marker == 1:
                    response = CH02_hagrid_REPLY_02_Negative
                    time.sleep(READ_DELAY)
                    milestone_marker = 2

                ##############################################
                #                  BLOCK 1                   #
                # Telling User about the basics              #
                ##############################################
                print(milestone_marker)
                if response_wit_parsed['intent'] == ['affirmative'] and milestone_marker == 0:
                    response = CH02_hagrid_REPLY_01_Postive
                    time.sleep(READ_DELAY)
                    milestone_marker = 1


                elif response_wit_parsed['intent'] == ['negative'] and milestone_marker == 0:
                    response = CH02_hagrid_REPLY_01_Negative
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

    slack_client_hagrid.procMsgSend(
        channel=IS_MSG_HANDLER_PORT,
        text=response,
        chapter=1,
        milestone=milestone_marker,
        dataType=slack_client_hagrid.IS_DATA,
        msgFrom=IS_HAGRID_PORT
    )
    return milestone_marker


def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_HAGRID in output['text']:
                # return text after the @ mention, whitespace removed
                # return output['text'].split(AT_BOT)[1].strip().lower(),
                return output['text'], \
                       output['channel']
    return None, None


# instantiate Slack & Twilio clients
slack_client_hagrid = procMsgInit(os.environ.get('SLACK_BOT_TOKEN_HAGRID'),IS_HAGRID_PORT)

if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    ##### Progression tracking #############
    milestone_marker = 0
    ########################################
    if slack_client_hagrid.procMsgConn():
        print("Hagrid Bot connected and running!")
        while True:
            command, channel = parse_slack_output(slack_client_hagrid.procMsgRecv())
            if command and channel:
                milestone_marker = handle_command(command, channel, milestone_marker)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
