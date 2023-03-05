import unittest
import sys
import datetime
import json
import pprint
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
sys.path.append(str(Path(__file__).parent.parent / "src"))
from src.webhook import app

def get_base_request():
    return {
        "version": "2.0",
        "routeKey": "$default",
        "rawPath": "/",
        "rawQueryString": "",
        "headers": {
            "content-length": "397",
            "x-amzn-tls-cipher-suite": "ECDHE-RSA-AES128-GCM-SHA256",
            "x-amzn-tls-version": "TLSv1.2",
            "x-line-signature": "XXXXXXXXXXX=",
            "x-amzn-trace-id": "Root=1-63fb0cf9-6ab0704968ba08566405ade3",
            "x-forwarded-proto": "https",
            "host": "XXXXXXXXXX.lambda-url.ap-northeast-1.on.aws",
            "x-forwarded-port": "443",
            "content-type": "application/json; charset=utf-8",
            "x-forwarded-for": "147.92.150.193",
            "user-agent": "LineBotWebhook/2.0"
        },
        "requestContext": {
            "accountId": "anonymous",
            "apiId": "XXXXXXXXXX",
            "domainName": "XXXXXXXXXX.lambda-url.ap-northeast-1.on.aws",
            "domainPrefix": "XXXXXXXXXX",
            "http": {
                "method": "POST",
                "path": "/",
                "protocol": "HTTP/1.1",
                "sourceIp": "147.92.150.193",
                "userAgent": "LineBotWebhook/2.0"
            },
            "requestId": "2599f942-7c76-43a7-ae5a-7138e8ddc5ef",
            "routeKey": "$default",
            "stage": "$default",
            "time": "26/Feb/2023:07:40:41 +0000",
            "timeEpoch": 1677397241914
        },
        "body": "",
        "isBase64Encoded": False
    }


class MyTestCase(unittest.TestCase):
    now: datetime.datetime = datetime.datetime.now()

    def test(self):
        # POST
        request = get_base_request()
        request['httpMethod'] = 'POST'
        request['path'] = '/v1/api/topics'
        line_body = {
            "destination": "U36e96084c6ff2c067e0805b16760ddf3",
            "events": [
                {
                    "type": "message",
                    "message": {
                        "type": "text",
                        "id": "17709823948205",
                        "text": "https://www.amazon.co.jp/%E5%AD%A4%E7%8B%AC%E3%81%AE%E3%82%B0%E3%83%AB%E3%83%A1-Season10/dp/B0B8Q3MZQZ"
                    },
                    "webhookEventId": "01GT6ANBY2M2DPM13QEQ46YJ9F",
                    "deliveryContext": {
                        "isRedelivery": False
                    },
                    "timestamp": 1677397241513,
                    "source": {
                        "type": "user",
                        "userId": "U5a0ab44ae87752a9c35370241b0b94fb"
                    },
                    "replyToken": "87c817c98f4d4c77938b6f9d0583c58b",
                    "mode": "active"
                }
            ]
        }
        request['body'] = json.dumps(line_body)

        response = app.lambda_handler(request, None)
        self.assertEqual(response, None)


if __name__ == '__main__':
    unittest.main()
