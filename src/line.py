import os
import json
import urllib.request

LINE_CHANNEL_ACCESS_TOKEN = os.environ.get('LINE_CHANNEL_ACCESS_TOKEN', None)


def reply(reply_token: str, message: str):
    url = 'https://api.line.me/v2/bot/message/reply'
    data = {
        'replyToken': reply_token,
        'messages': [
            {
                'type': 'text',
                'text': message
            }
        ]
    }
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + LINE_CHANNEL_ACCESS_TOKEN
    }
    req = urllib.request.Request(url, json.dumps(data).encode(), headers)
    with urllib.request.urlopen(req) as res:
        print(f'{res.read()}')


def multicast(message: str, user_ids: list[str]):
    url = 'https://api.line.me/v2/bot/message/multicast'
    data = {
        'to': user_ids,
        'messages': [
            {
                'type': 'text',
                'text': message
            }
        ]
    }
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + LINE_CHANNEL_ACCESS_TOKEN
    }
    req = urllib.request.Request(url, json.dumps(data).encode(), headers)
    with urllib.request.urlopen(req) as res:
        print(f'{res.read()}')

