import os
import time
from slackclient import SlackClient
from utils import wit_response, wit_petunia_response

# starterbot's ID as an environment variable
BOT_ID_PETUNIA = 'U7JK660E6'
#BOT_ID_PETUNIA = os.environ.get("BOT_ID_PETUNIA")
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

#random
READ_DELAY = 2


def handle_command(command, channel):
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

        #response += START_COMMAND
        if general_text == START_COMMAND:
            response = AT_DUDLEY + "Dudders when was the last time you received a hair cut?"
            time.sleep(READ_DELAY)
            check = True

        if general_text == RESPONSE_1:
            response = AT_DUDLEY + "Oh sweetums, I know you don't want to go, but we'll get Harry to " \
                       "schedule it."
            time.sleep(READ_DELAY)
            check = True

        if general_text == RESPONSE_2:
            response = AT_HP + "Well...Boy, were you listening?! BOY! Didn't you hear my sweetums. Get on with it!"
            time.sleep(READ_DELAY)
            check = True

        ##########
        # WIT.AI #
        ##########
        if not check:

            entity, value = wit_petunia_response(command)

            response = "BOO" + entity + " " + value

            if entity == 'intent' and value == 'dudley_is_scared':
                response = "NOT IN THIS HOUSE POTTER!!!"
                time.sleep(READ_DELAY)
            elif entity == 'object_of_fear':
                response = "Did you say {}?! Not in this household POTTER!".format(str(value))
                time.sleep(READ_DELAY)
            elif entity == 'object_of_protection':
                response = "Don't worry Dudders {} is here. POTTER! GET OUT NOW!".format(str(value))
                time.sleep(READ_DELAY)

            if entity is None:
                response = "Harry go to CUPBOARD UNDER THE STAIRS NOW!!!"
                time.sleep(READ_DELAY)

    slack_client_petunia.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)


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
slack_client_petunia = SlackClient(os.environ.get('SLACK_BOT_TOKEN_PETUNIA'))

if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client_petunia.rtm_connect():
        print("Aunt Petunia Bot connected and running!")
        while True:
            command, channel = parse_slack_output(slack_client_petunia.rtm_read())
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")