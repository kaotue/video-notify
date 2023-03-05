import boto3
from boto3.dynamodb.conditions import Key, Attr
import os
from bs4 import BeautifulSoup
import json
import urllib

table = boto3.resource('dynamodb').Table(os.environ.get('TABLE_NAME', 'vn-dev-table'))
LINE_CHANNEL_ACCESS_TOKEN = os.environ.get('LINE_CHANNEL_ACCESS_TOKEN', None)


def lambda_handler(event, context) -> dict:
    print(f'{event=}')
    print(f'{context=}')
    run_batch()


def run_batch():
    for video_id in get_video_ids():
        print(f'{video_id=}------------------------------')
        url = f'https://www.amazon.co.jp/gp/video/detail/{video_id}/'
        soup = get_soup(url)
        title = get_title(soup)
        print(f'{title=}')

        latest_ep_db = get_latest_ep_from_db(video_id)
        print(f'{latest_ep_db=}')
        latest_ep_web = get_latest_ep_from_web(soup)
        print(f'{latest_ep_web=}')

        if latest_ep_db == latest_ep_web:
            continue
        post_video_db(video_id, title, latest_ep_web)
        target_user_ids = get_user_ids_by_video_id(video_id)
        if not target_user_ids:
            continue

        if latest_ep_db < latest_ep_web:
            message = f'{title}\n新エピソード{latest_ep_web}話が配信されました。\n{url}'
            multicast_line_channel(message, target_user_ids)
            print('streaming start ㊗️')
        elif latest_ep_db > latest_ep_web:
            message = f'{title}\n配信が停止されました。\n{url}'
            multicast_line_channel(message, target_user_ids)
            print('streaming stop ⚠️')


def get_soup(url: str):
    req = urllib.request.Request(url)
    req.add_header('User-Agent',
                   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36')
    response = urllib.request.urlopen(req)
    soup = BeautifulSoup(response, 'html.parser')
    return soup


def get_title(soup) -> str:
    if not (results := soup.select('*[data-automation-id="title"]')):
        return None
    return results[0].text


def get_latest_ep_from_web(soup) -> int:
    if not is_streaming_top(soup):
        return -1
    if not (ep_list := soup.select('li[id^=av-ep-episodes-]')):
        return -1
    print_list = []
    for ep in reversed(ep_list):
        ep_num = int(ep['id'].split('-')[-1]) + 1
        if is_streaming(ep):
            print_list.append(str(ep_num) + '🆗')
            print('ep:' + ','.join(print_list))
            return ep_num
        print_list.append(str(ep_num) + '🈳')
    print('ep:' + ','.join(print_list))
    return -1


def is_streaming_top(soup) -> bool:
    if not (top := soup.select('div[id="dv-action-box"]')):
        return False
    if top[0].select('a[href*="/gp/video/signup"]'):
        return True
    if top[0].select('a[href*="/gp/video/detail"]'):
        return True
    if top[0].select('a[href*="signup"]'):
        return True
    return False


# get ep is streaming from href
def is_streaming(ep) -> bool:
    if ep.select('a[href*="/gp/video/signup"]'):
        return True
    elif ep.select('a[href*="/gp/video/detail"]'):
        return True
    elif ep.select('a[href*="signup"]'):
        return True
    else:
        return False


# get video id from url
def get_video_id(url: str) -> str:
    resources = url.split('/detail/')
    if not resources or len(resources) < 2:
        resources = url.split('/dp/')
        if not resources or len(resources) < 2:
            return None
    if not (resources := resources[1].split('/')):
        return None
    return resources[0]


def get_latest_ep_from_db(video_id: str) -> int:
    response = table.get_item(
        Key={
            'id': 'video@',
            'sub_id': video_id
        }
    )
    if not response.get('Item'):
        print(f'video id is not found: {video_id=}')
        return -1
    return int(response['Item']['latest_ep'])


def get_user_ids_by_video_id(video_id: str) -> list[str]:
    response = table.query(
        KeyConditionExpression=Key('id').eq('videouser@') & Key('sub_id').begins_with(video_id + '@')
    )
    if not response.get('Items'):
        None
    return [x['sub_id'].split('@')[1] for x in response['Items']]


def get_video_ids():
    response = table.query(
        KeyConditionExpression=Key('id').eq('video@')
    )
    if not response.get('Items'):
        None
    return [x['sub_id'] for x in response['Items']]


def post_video_db(video_id: str, title: str, latest_ep: int):
    table.put_item(
        Item={
            'id': 'video@',
            'sub_id': video_id,
            'title': title,
            'latest_ep': latest_ep
        })


def post_line_channel(reply_token: str, message: str):
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


def multicast_line_channel(message: str, user_ids: list[str]):
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
