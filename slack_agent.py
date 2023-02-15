import time

from slack import WebClient
from slack.errors import SlackApiError

from utils import say, USERS, ROBOT_ID


class SlackClient:
    def __init__(self, token_str, channel_id, ssl_context):
        self.token = token_str
        self.channel = channel_id
        self.ssl_context = ssl_context

        self.client = WebClient(
            token=token_str,
            ssl=ssl_context)

    def post_message(self, message):
        try:
            _ = self.client.chat_postMessage(
                link_names=True,
                channel=self.channel,
                text=message)
        except SlackApiError as e:
            assert e.response["ok"] is False
            assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
            print(f"Got an error: {e.response['error']}")

    def listen_for_message(self):
        try:
            last_time = ''
            while True:
                message = self.client.conversations_history(channel=self.channel, limit=1)
                print(message['messages'][0])
                if 'bot_id' in message['messages'][0] \
                        and message['messages'][0]['bot_id'] == ROBOT_ID \
                        and last_time != message['messages'][0]['text']:

                    last_time = message['messages'][0]['text']
                    if last_time.startswith('<@'):
                        sentence = last_time.replace('<@', '').replace('>', '')
                        name = sentence.split(' ')[0]
                        sentence = sentence.replace(name, USERS[name])
                        print(sentence)
                        say(sentence)
                        if name == 'ROBOT_ID':
                            say('小丑竟是我自己', lang_version=1)
                    else:
                        print(last_time)
                        say(last_time)
                time.sleep(1)
        except SlackApiError as e:
            assert e.response["ok"] is False
            assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
            print(f"Got an error: {e.response['error']}")
