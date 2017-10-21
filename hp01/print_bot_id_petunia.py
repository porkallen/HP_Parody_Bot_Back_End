import os
from slackclient import SlackClient


BOT_NAME_PETUNIA = 'petunia'

slack_client_petunia = SlackClient(os.environ.get('SLACK_BOT_TOKEN_PETUNIA'))


if __name__ == "__main__":
    api_call = slack_client_petunia.api_call("users.list")
    if api_call.get('ok'):
        # retrieve all users so we can find our bot
        users = api_call.get('members')
        for user in users:
            print(user['name'])
            if 'name' in user and user.get('name') == BOT_NAME_PETUNIA:
                print("Bot ID for '" + user['name'] + "' is " + user.get('id'))
    else:
        print("could not find bot user with the name " + BOT_NAME_PETUNIA)