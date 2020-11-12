import unittest
import io
import inspect
import os

# See: https://stackoverflow.com/questions/1218933/can-i-redirect-the-stdout-in-python-into-some-sort-of-string-buffer
from contextlib import redirect_stdout

# Import the 'main function from word_index.py as wi_main
from word_index import main as wi_main

# Find ../test-data. Note there are two os.path.dirname

TEST_DATA = os.path.join(os.path.dirname(os.path.dirname(os.path.normpath(os.path.realpath(__file__)))), "test-data")

class TestWordIndex(unittest.TestCase):
    def test_output_with_an_empty_file_produces_not_output(self):
        print(inspect.stack()[0][3]) # Print the name of THIS function

        # Execute main and be sure you capture the output
        with io.StringIO() as buf, redirect_stdout(buf):
            wi_main(os.path.join(TEST_DATA, './empty.txt'))
            output = buf.getvalue()

        # Check the output is not None
        self.assertIsNotNone(output, msg="Output cannot be None")

        # Check the output is not empty
        self.assertEqual(output, '', msg="Output is not empty")

    def test_output_with_another_one_line_file(self):
        print(inspect.stack()[0][3])

        # Execute main and be sure you capture the output
        with io.StringIO() as buf, redirect_stdout(buf):
            wi_main(os.path.join(TEST_DATA, './one-line.txt'))
            output = buf.getvalue()

        # Check the output is the expected one.
        # Q: Do we care about the last '\n' ?
        self.assertEqual(output, "blablba - 1\n", msg="Output cannot be empty")

    def test_frequent_word_is_filtered(self):
        print(inspect.stack()[0][3])

        # Execute main and be sure you capture the output
        with io.StringIO() as buf, redirect_stdout(buf):
            wi_main(os.path.join(TEST_DATA, './test.txt'))
            output = buf.getvalue()

        # Check the output is the expected one.
        # https://kapeli.com/cheat_sheets/Python_unittest_Assertions.docset/Contents/Resources/Documents/index
        self.assertNotIn("Line", output, msg="Output contains filtered word")

if __name__ == '__main__':
    unittest.main()


