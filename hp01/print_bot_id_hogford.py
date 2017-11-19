import os
from slackclient import SlackClient


BOT_NAME_HOGFORD = 'hogford'

slack_client_hogford = SlackClient('xoxb-260347880417-cykm48o6jvV2Zu604TTVTG3h')


if __name__ == "__main__":
    api_call = slack_client_hogford.api_call("users.list")
    if api_call.get('ok'):
        # retrieve all users so we can find our bot
        users = api_call.get('members')
        for user in users:
            print(user['name'])
            if 'name' in user and user.get('name') == BOT_NAME_HOGFORD:
                print("Bot ID for '" + user['name'] + "' is " + user.get('id'))
    else:
        print("could not find bot user with the name " + BOT_NAME_HOGFORD)