import unittest
import sys
import datetime
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
sys.path.append(str(Path(__file__).parent.parent / "src"))
from src import app_batch


class MyTestCase(unittest.TestCase):
    now: datetime.datetime = datetime.datetime.now()

    def test(self):
        test_event = {}
        test_event['is_debug'] = True
        response = app_batch.lambda_handler(test_event, None)

        self.assertEqual(response, None)


if __name__ == '__main__':
    unittest.main()
