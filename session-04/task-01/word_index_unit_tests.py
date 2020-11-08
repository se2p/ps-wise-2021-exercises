import unittest
import sys

# Import the 'main function from word_index.py as wi_main
from word_index import main as wi_main

class TestPythonVersion(unittest.TestCase):

    def test_python_version(self):
        """ This is a simple example of a unittest that checks if you are running the right version of Python """
        self.assertEqual(sys.version_info.major, 3, msg="You are not running python 3")
        self.assertEqual(sys.version_info.minor, 7, msg="You are not running python 3.7")

if __name__ == '__main__':
    unittest.main()