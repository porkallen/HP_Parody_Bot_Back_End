import os
import time
from slackclient import SlackClient
from utils import wit_response

# starterbot's ID as an environment variable
BOT_ID_PETUNIA = 'U7JK660E6'
BOT_ID_DUDLEY = 'U7JL8RLEQ'
BOT_ID = 'U7HQ4QJR2'
#BOT_ID = os.environ.get("BOT_ID")

# constants
AT_BOT = "<@" + BOT_ID + ">"
AT_PETUNIA = "<@" + BOT_ID_PETUNIA + ">"
AT_DUDLEY = "<@" + BOT_ID_DUDLEY + ">"
EXAMPLE_COMMAND = "do"


def handle_command(command, channel):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """
    response = "Not sure what you mean. Use the *" + EXAMPLE_COMMAND + \
               "* command with numbers, delimited by spaces."

    if command.startswith(AT_BOT):
        general_text = command.split(AT_BOT)[1].strip().lower()
        response = "Yes... I heard you Aunt Petunia..."
    '''''
    if command.startswith(EXAMPLE_COMMAND):

        response = None

        entity, value = wit_response(command)

        if entity == 'class_type':
            response = "Oh I love {}!".format(str(value))
        elif entity == 'house_type':
            response = "Oh {}, I love them!".format(str(value))

        if entity is None:
            response = "Stop being a muggle"

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

    slack_client.api_call("chat.postMessage", channel=channel,
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
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("StarterBot connected and running!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")