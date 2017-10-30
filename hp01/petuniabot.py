import os
import time
from utils import wit_response, wit_petunia_response
from procComm import *
from botMap import *

# starterbot's ID as an environment variable
BOT_ID_PETUNIA = os.environ.get("BOT_ID_PETUNIA")
BOT_ID_DUDLEY = 'U7JL8RLEQ'
BOT_ID = 'U7HQ4QJR2'

# constants
AT_BOT = "<@" + BOT_ID_PETUNIA + ">"
AT_DUDLEY = "<@" + BOT_ID_DUDLEY + ">"
AT_HP = "<@" + BOT_ID + ">"

# rails
EXAMPLE_COMMAND = "do"
START_COMMAND = "bot exec"
RESPONSE_1 = "mom stop it i'm watching the tele!"
RESPONSE_2 = "fine... mother... but only because harry is scheduling it!"
RESPONSE_3 = "mom stop talking i'm watching the tele, trump is on! he is firing people on the apprentice!"

# rails - block 1.5
STATEMENT_04 = "STOP TEXTING ME AND START TEXTING BOB YOU FOOLISH BOY!"

# rails - block 2
STATEMENT_05 = "What? How DARE YOU?! Who told you -- Dudders close your ears! I don't want you to hear anything about " \
               "this SCIENCE nonsense. Just go back to watching the Tele... Wait just one moment... Sweetums... What" \
               "are you watching on the Tele?"

STATEMENT_06 = "Oh thank goodness! Dudders you are so brilliant, you know you are learning a lot watching his show." \
               "Trump knows how to be a true leader he is not distracted by this science nonsense... " \
               "If only he could lead a country one day... "

#random
READ_DELAY = 2


def handle_command(command, channel, milestone_marker):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """
    response = "EXECUSE ME!! You UNGRATEFUL little BRAT! Use proper English " \
               "when talking to me!"

    if command.startswith(AT_BOT):

        check = False
        general_text = command.split(AT_BOT)[1].strip().lower()

        #ENTRY BLOCK OF CODE NO MILSETONE CHECK NEEDED

        # @Doby, I seperated this into Non Wit and Wit section... but I think it needs to be organized better.
        # @Doby, The flow is a bit odd because I go back and forth. Look at Block 2 for example.

        ##############################################
        #                  BLOCK 0                   #
        # This is what the bot intialize says        #
        ##############################################
        if general_text == START_COMMAND:
            response = AT_DUDLEY + "Dudders when was the last time you received a hair cut?"
            time.sleep(READ_DELAY)
            check = True
            milestone_marker = 0

        if general_text == RESPONSE_1:
            response = AT_DUDLEY + "Oh sweetums, I know you don't want to go, but we'll get Harry to " \
                       "schedule it."
            time.sleep(READ_DELAY)
            check = True

        if general_text == RESPONSE_2:
            response = AT_HP + "Well...Boy, were you listening?! BOY! Didn't you hear my sweetums. Get on with it!"
            time.sleep(READ_DELAY)
            check = True
            milestone_marker = 1

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


        ##########
        # WIT.AI #
        ##########
        if not check:

            response_wit_parsed = wit_petunia_response(command)

            response = "Made it this far"

            print(response_wit_parsed)

            #First checking to see if Wit picked up an intent
            if 'intent' in response_wit_parsed:
                ##############################################
                #                  BLOCK 1.5                 #
                # Waiting for user to respond about hair cut #
                ##############################################
                print(milestone_marker)
                if response_wit_parsed['intent'] == ['affirmative'] and milestone_marker == 1:
                    response = STATEMENT_04
                    time.sleep(READ_DELAY)
                    milestone_marker = 2
                    # @Doby once this marker is reached the script for Bob's haircut should start (not yet written)
                    # @Doby, so just skip to the Hogwarts script running

                ###################################################
                #                  BLOCK 2                        #
                # This is after Harry has heard back from Hogford #
                ###################################################
                if response_wit_parsed['intent'] == ['hogford_question'] and milestone_marker == 2:
                    response = AT_DUDLEY + STATEMENT_05
                    time.sleep(READ_DELAY)
                    milestone_marker = 3

                ##############################################
                #                  BLOCK X                   #
                # This Block is to catch RANDOM phrases      #
                ##############################################
                if response_wit_parsed['intent'] == ['dudley_is_scared']:
                    response = "NOT IN THIS HOUSE POTTER!!!"
                    time.sleep(READ_DELAY)
                    if 'object_of_fear' in response_wit_parsed:
                        response = "Did you say {}?! Not in this household POTTER!".format(str(response_wit_parsed['object_of_fear'][0]))
                        time.sleep(READ_DELAY)
                    if 'object_of_protection' in response_wit_parsed:
                        response = "Don't worry Dudders {} is here. POTTER! GET OUT NOW!".format(str(response_wit_parsed['object_of_protection'][0]))
                        time.sleep(READ_DELAY)

            else:
                response = "Harry go to CUPBOARD UNDER THE STAIRS NOW!!!"
                time.sleep(READ_DELAY)

    slack_client_petunia.procMsgSend(channel=IS_MSG_HANDLER_PORT,text=response,dataType=slack_client_petunia.IS_DATA)
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
            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                # return output['text'].split(AT_BOT)[1].strip().lower(),
                return output['text'], \
                       output['channel']
    return None, None


# instantiate Slack & Twilio clients
slack_client_petunia = procMsgInit(os.environ.get('SLACK_BOT_TOKEN_PETUNIA'),IS_PETUNIA_PORT)

if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    ##### Progression tracking #############
    milestone_marker = 0
    ########################################
    if slack_client_petunia.procMsgConn():
        print("Aunt Petunia Bot connected and running!")
        while True:
            command, channel = parse_slack_output(slack_client_petunia.procMsgRecv())
            if command and channel:
                milestone_marker = handle_command(command, channel, milestone_marker)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")