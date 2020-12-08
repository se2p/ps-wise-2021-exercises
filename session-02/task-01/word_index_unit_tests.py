import unittest
import io
import inspect
import os


# Import the 'main function from word_index.py as wi_main
from word_index import main as wi_main

# We need to create three unit tests that make use of temp files/folders
# https://simpleit.rocks/python/test-files-creating-a-temporal-directory-in-python-unittests/
import tempfile

# See: https://stackoverflow.com/questions/1218933/can-i-redirect-the-stdout-in-python-into-some-sort-of-string-buffer
from contextlib import redirect_stdout


class TestWordIndexUsingTempFiles(unittest.TestCase):

    test_dir = None

    # This is executed automatically before every test
    def setUp(self):
        # Create a temporary directory
        self.test_dir = tempfile.TemporaryDirectory()

    # This is executed automatically after every test
    def tearDown(self):
        # Remove the tempdir
        self.test_dir.cleanup()

    def test_program_with_no_lines(self):
        # Print name of this test
        print(inspect.stack()[0][3])

        temp_file = os.path.join(self.test_dir.name, "empty.txt")

        with open(temp_file, 'w') as f:
            f.writelines("")

        expected_output = "" #'\n'.join([""])

        with io.StringIO() as buf, redirect_stdout(buf):
            # Invoke main passing the temp file
            wi_main(temp_file)
            output = buf.getvalue()

        # Make the assertions
        self.assertEqual(output, expected_output, msg="Output does not match")

    def test_program_with_few_lines(self):
        # Print name of this test
        print(inspect.stack()[0][3])

        temp_file = os.path.join(self.test_dir.name, "input.txt")

        with open(temp_file, 'w') as f:
            f.writelines('\n'.join(["foo", "bar"]))

        expected_output = '\n'.join(["bar - 1", "foo - 1",""])

        with io.StringIO() as buf, redirect_stdout(buf):
            # Invoke main passing the temp file
            wi_main(temp_file)
            output = buf.getvalue()

        # Make the assertions
        self.assertEqual(output, expected_output, msg="Output does not match")

    def test_that_overly_recurrent_words_are_not_reported(self):

        # Print name of this test
        print(inspect.stack()[0][3])

        temp_file = os.path.join(self.test_dir.name, "input.txt")

        with open(temp_file, 'w') as f:
            f.writelines('\n'.join(["foo", "bar", "bar", "bar", "bar"]))

        expected_output = '\n'.join(["foo - 1", ""])

        with io.StringIO() as buf, redirect_stdout(buf):
            # Invoke main passing the temp file.
            wi_main(temp_file, STOP_FREQUENCY_LIMIT=3)

            output = buf.getvalue()

        # Make the assertions
        self.assertEqual(output, expected_output, msg="Output does not match")

if __name__ == '__main__':
    unittest.main()