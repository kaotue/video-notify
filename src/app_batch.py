import importlib
import line
import table
import utils


def lambda_handler(event, context):
    if event.get('is_debug', None):
        line = importlib.import_module('line_debug')

    for video_id in table.get_video_ids():
        print(f'{video_id=}------------------------------')
        url = f'https://www.amazon.co.jp/gp/video/detail/{video_id}/'
        soup = utils.get_soup(url)
        title = utils.get_title(soup)
        print(f'{title=}')

        latest_ep_db = table.get_latest_ep(video_id)
        print(f'{latest_ep_db=}')
        latest_ep_web = utils.get_latest_ep(soup)
        print(f'{latest_ep_web=}')

        if latest_ep_db == latest_ep_web:
            continue
        table.post_video(video_id, title, latest_ep_web)
        target_user_ids = table.get_user_ids_by_video_id(video_id)
        if not target_user_ids:
            continue

        if latest_ep_db < latest_ep_web:
            message = f'{title}\n新エピソード{latest_ep_web}話が配信されました🎉\n{url}'
            line.multicast(message, target_user_ids)
            print('streaming start 🎉')
        elif latest_ep_db > latest_ep_web:
            message = f'{title}\n配信が停止された、もしくはページを読み込めませんでした🚫\n{url}'
            line.multicast(message, target_user_ids)
            print('streaming stop 🚫')



