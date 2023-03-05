import os
import boto3
from boto3.dynamodb.conditions import Key, Attr

table = boto3.resource('dynamodb').Table(os.environ.get('TABLE_NAME', 'vn-dev-table'))


def post_video(video_id: str, title: str, latest_ep: int):
    table.put_item(
        Item={
            'id': 'video@',
            'sub_id': video_id,
            'title': title,
            'latest_ep': latest_ep
        })


def post_user_video(user_id: str, video_id: str):
    table.put_item(
        Item={
            'id': 'videouser@',
            'sub_id': video_id + '@' + user_id
        })


def get_latest_ep(video_id: str) -> int:
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


def exists_user_video(user_id: str, video_id: str):
    response = table.query(
        KeyConditionExpression=Key('id').eq('videouser@') & Key('sub_id').eq(video_id + '@' + user_id)
    )
    if response.get('Items'):
        return True
    else:
        return False


def exists_video(video_id: str):
    response = table.query(
        KeyConditionExpression=Key('id').eq('video@') & Key('sub_id').eq(video_id)
    )
    if response.get('Items'):
        return True
    else:
        return False
