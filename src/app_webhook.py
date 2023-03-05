import importlib
import json
import line
import table
import utils


def lambda_handler(event, context) -> dict:
    if event.get('is_debug', None):
        line = importlib.import_module('line_debug')

    if not (body := event.get('body')):
        return 'invalid request'

    json_body = json.loads(body)
    print(f'{json_body=}')
    line_event = json_body['events'][0]
    if line_event['type'] == 'message':
        main_logic_message(line_event)
    else:
        print(f'invalid message type: {line_event["type"]}')
        return 'invalid message type'
    return 'success'


def main_logic_message(line_event: dict):
    user_id = line_event['source']['userId']
    message = line_event['message']['text']
    reply_token = line_event['replyToken']

    if not (message.startswith('https://')):
        line.reply(
            reply_token=reply_token,
            message='新エピソード公開時に、通知を受けたいURLを貼り付けてください。'
        )
        return
    if not (video_id := utils.get_video_id(message)):
        line.reply(
            reply_token=reply_token,
            message='有効なページではありませんでした。'
        )
        return

    url = f'https://www.amazon.co.jp/gp/video/detail/{video_id}/'

    if not table.exists_video(video_id):
        post_new_video(url)
    if not table.exists_user_video(user_id, video_id):
        table.post_user_video(user_id, video_id)
        line.reply(
            reply_token=reply_token,
            message='通知登録しました🎉'
        )
    else:
        line.reply(
            reply_token=reply_token,
            message='あなたは既にこの動画の通知登録をされています。'
        )


def post_new_video(url):
    video_id = utils.get_video_id(url)
    print(f'{video_id=}')
    soup = utils.get_soup(url)
    title = utils.get_title(soup)
    print(f'{title=}')
    latest_ep_web = utils.get_latest_ep(soup)
    print(f'{latest_ep_web=}')
    table.post_video(video_id, title, latest_ep_web)







