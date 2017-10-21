import os
from slackclient import SlackClient


BOT_NAME_DUDLEY = 'dudley'

slack_client_dudley = SlackClient(os.environ.get('SLACK_BOT_TOKEN_DUDLEY'))


if __name__ == "__main__":
    api_call = slack_client_dudley.api_call("users.list")
    if api_call.get('ok'):
        # retrieve all users so we can find our bot
        users = api_call.get('members')
        for user in users:
            print(user['name'])
            if 'name' in user and user.get('name') == BOT_NAME_DUDLEY:
                print("Bot ID for '" + user['name'] + "' is " + user.get('id'))
    else:
        print("could not find bot user with the name " + BOT_NAME_DUDLEY)