import unittest
import sys
import datetime
import json
import pprint
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
sys.path.append(str(Path(__file__).parent.parent / "src"))
from src.batch import app


class MyTestCase(unittest.TestCase):
    now: datetime.datetime = datetime.datetime.now()

    # def test(self):
    #     url = 'https://www.amazon.co.jp/%E5%AD%A4%E7%8B%AC%E3%81%AE%E3%82%B0%E3%83%AB%E3%83%A1-Season10/dp/B0B8Q3MZQZ'
    #     video_id = app.get_video_id(url)
    #     print(f'{video_id=}')
    #     soup = app.get_soup(url)
    #     title = app.get_title(soup)
    #     print(f'{title=}')
    #     ep_web = app.get_latest_ep_from_web(soup)
    #
    #     self.assertTrue(ep_web)

    def test2(self):
        app.run_batch()
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
