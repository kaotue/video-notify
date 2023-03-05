import unittest
import sys
import datetime
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
sys.path.append(str(Path(__file__).parent.parent / "src"))
from src import utils


class MyTestCase(unittest.TestCase):
    now: datetime.datetime = datetime.datetime.now()

    def test_get_latest_ep(self):
        url = 'https://www.amazon.co.jp/%E5%AD%A4%E7%8B%AC%E3%81%AE%E3%82%B0%E3%83%AB%E3%83%A1-Season10/dp/B0B8Q3MZQZ'
        video_id = utils.get_video_id(url)
        print(f'{video_id=}')
        soup = utils.get_soup(url)
        title = utils.get_title(soup)
        print(f'{title=}')
        ep_web = utils.get_latest_ep(soup)
        print(f'{ep_web=}')

        self.assertTrue(ep_web)


if __name__ == '__main__':
    unittest.main()
