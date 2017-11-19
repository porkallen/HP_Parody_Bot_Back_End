import os
import time
from utils import wit_response, wit_dudley_response
from procComm import *
from botMap import *

# starterbot's ID as an environment variable
BOT_ID_PETUNIA = 'U7JK660E6'
BOT_ID_DUDLEY = os.environ.get("BOT_ID_DUDLEY")
BOT_ID = 'U7HQ4QJR2'

# constants
AT_BOT = "<@" + BOT_ID_DUDLEY + ">"
AT_HP = "<@" + BOT_ID + ">"
AT_PETUNIA = "<@" + BOT_ID_PETUNIA + ">"

# rails
EXAMPLE_COMMAND = "do"
QUESTION_1 = "dudders when was the last time you received a hair cut?"
QUESTION_2 = "oh sweetums, i know you don't want to go, but we'll get harry to " \
             "schedule it."

QUESTION_3 = "what? how dare you?! who told you -- dudders close your ears! i don't want you to hear anything about " \
               "this science nonsense. just go back to watching the tele... wait just one moment... sweetums... what" \
               "are you watching on the tele?"

STATEMENT_3 = "Mom stop talking I'm watching the Tele, Trump is on! He is firing people on The Apprentice!"

#random
READ_DELAY = 2

def handle_command(command, channel):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """
    response = "HAHAHA Potter doesn't even know how to speak English good! Potter more like... NOT SMART!"

    ##### NEEED TO FIX THE TRUE FALSE TAGS BAD STRUCTURE###
    if command.startswith(AT_BOT):
        check = False
        general_text = command.split(AT_BOT)[1].strip().lower()

        if general_text == QUESTION_1:
            response = AT_PETUNIA + "Mom stop it I'm watching the Tele!"
            time.sleep(READ_DELAY)
            check = True

        if general_text == QUESTION_2:
            response = AT_PETUNIA + "Fine... Mother... but only because Harry is scheduling it!"
            time.sleep(READ_DELAY)
            check = True

        print(general_text)
        if general_text == QUESTION_3:
            response = AT_PETUNIA + STATEMENT_3
            time.sleep(READ_DELAY)
            check = True

        ##########
        # WIT.AI #
        ##########
        if not check:

            response_wit_parsed = wit_dudley_response(command)

            #First checking to see if Wit picked up an intent
            if 'intent' in response_wit_parsed:
                #Second, since it picked up an intent it needs to see wht it is
                if response_wit_parsed['intent'] == ['insult']:
                    #Third, I need to see if the intent has an object or sub section
                    if 'object_of_insult' in response_wit_parsed:
                        #counting how many objects in sub section
                        how_many_insults = len(response_wit_parsed['object_of_insult'])
                        if how_many_insults == 1:
                            response = "Shut Up Potter, you are a {}!".format(
                                str(response_wit_parsed['object_of_insult'][0]))
                        if how_many_insults == 2:
                            response = "Shut Up Potter, you are a {} and a {}!".format(
                                str(response_wit_parsed['object_of_insult'][0]),str(response_wit_parsed['object_of_insult'][1]))
                        if how_many_insults >= 3:
                            response = "Shut Up {}, you are a {}!".format(
                                str(response_wit_parsed['object_of_insult'][0]), str(response_wit_parsed['object_of_insult'][2]))
                    else:
                        response = "Shut Up POTTER, you don't even know how to make a good insult!"

                #Second, the other option for intent
                elif response_wit_parsed['intent'] == ['threaten_with_magic']:
                    #If Wit was able to pick up an object
                    if 'object_attacking_with' in response_wit_parsed:
                        response = AT_PETUNIA + "Are you talking about magic?! Mummy! Mummy! Harry is " \
                                            "talking about {}!".format(str(response_wit_parsed['object_attacking_with'][0]))
                    else:
                        response = AT_PETUNIA + "Are you talking about magic?! Mummy! Mummy! Harry is " \
                                                "talking about SCARY magic!"

                #Third, the other option for intent
                elif response_wit_parsed['intent'] == ['attack_with_magic']:
                    #If Wit was able to pick up an object
                    if 'spell_attacking_with' in response_wit_parsed:
                        how_many_spells = len(response_wit_parsed['spell_attacking_with'])
                        if how_many_spells > 1:
                            response = "AHHHHH!!!"
                        else:
                            response = AT_PETUNIA + "AHHHHHH Mummy! Mummy! Harry is using magic!"
                    else:
                        response = AT_PETUNIA + "AHHHHHH Mummy! Mummy! Harry is PROBABLY usinging magic!"
            else:
                response = "Harry you are A BIG STUPID IDIOT!!!!"
                time.sleep(READ_DELAY)


            ######################################
            # Need to Redo all the logic here... #
            ######################################
            '''''
            if entity == 'intent' and value == 'insult':
                response = "Shut Up Potter, you are a {}!".format(str(value))
                time.sleep(READ_DELAY)
            elif entity == 'intent' and value == 'threaten_with_magic':
                response = AT_PETUNIA + "Are you talking about magic?! Mummy! Mummy! Harry is " \
                                        "talking about {}!".format(str(value))
                time.sleep(READ_DELAY)
            #Can remove this dupe when i have dictionaries
            elif entity == 'object_attacking_with':
                response = AT_PETUNIA + "Are you talking about magic?! Mummy! Mummy! Harry is " \
                                        "talking about {}!".format(str(value))
                time.sleep(READ_DELAY)
            elif entity == 'object_of_insult':
                response = "Shut Up Potter, you are a {}!".format(str(value))
                time.sleep(READ_DELAY)

            if entity is None:
                response = "Harry you are A BIG STUPID IDIOT!!!!"
                time.sleep(READ_DELAY)


        words = command.split()
        for word in words:
            check = word
            if word == 'cool':
                response ="Niceeeeee"
            elif word == 'hogwarts':
                response = "I went there!"
            elif word == 'hermoine':
                response = "That is my best friend! Maybe even more than my best friend..."

        response = entity + value
        '''''
        slack_client_dudley.procMsgSend(
            channel = IS_MSG_HANDLER_PORT,
            text = response,
            chapter = 0,
            milestone = 0,
            dataType=slack_client_dudley.IS_DATA,
        
        )


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
#slack_client_dudley = SlackClient(os.environ.get('SLACK_BOT_TOKEN_DUDLEY'))
slack_client_dudley = procMsgInit(os.environ.get('SLACK_BOT_TOKEN_DUDLEY'),IS_DUDLEY_PORT)

if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client_dudley.procMsgConn():
        print("Dudley Bot connected and running!")
        while True:
            command, channel = parse_slack_output(slack_client_dudley.procMsgRecv())
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")