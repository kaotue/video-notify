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

    def test(self):
        response = app.lambda_handler(None, None)
        self.assertEqual(response, None)


if __name__ == '__main__':
    unittest.main()
