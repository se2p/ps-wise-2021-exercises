import unittest
import io
import inspect

# See: https://stackoverflow.com/questions/1218933/can-i-redirect-the-stdout-in-python-into-some-sort-of-string-buffer
from contextlib import redirect_stdout

from unittest.mock import patch, mock_open

# Import the program under test.
# Q: If I move the import INSIDE the test, e.g., setUp, will the global variables automatically re-evaluated?
from word_index import main as wi_main


class TestWordIndexUsingMocks(unittest.TestCase):

    def test_output_with_a_mocked_file(self):
        print(inspect.stack()[0][3])

        fake_file_path="/fake/file/path"

        lines = ["foo", "bar"]

        fake_file = io.StringIO('\n'.join(lines))

        # Execute main and be sure you capture the output but use mocking to fake a file read by the program
        with io.StringIO() as buf, redirect_stdout(buf):

            # Moking in action
            with patch('word_index.open', return_value=fake_file, create=True):
                wi_main(fake_file_path)

            output = buf.getvalue()

        # Check the output is not None
        self.assertIsNotNone(output, msg="Output cannot be None")

        # Check the output is not empty
        self.assertNotEqual(output, '', msg="Output cannot be empty")

        # Check output is as we expect
        self.assertEqual(output, 'bar - 1\nfoo - 1\n', msg="Output cannot be empty")

    def test_output_with_empty_file(self):
        print(inspect.stack()[0][3])

        fake_file_path="/fake/file/path"
        lines = [""]
        fake_file = io.StringIO('\n'.join(lines))

        # Execute main and be sure you capture the output but use mocking to fake a file read by the program
        with io.StringIO() as buf, redirect_stdout(buf):
            with patch('word_index.open', return_value=fake_file, create=True):
                wi_main(fake_file_path)

            output = buf.getvalue()

        # Check the output is not None
        self.assertIsNotNone(output, msg="Output cannot be None")

        # Check the output is INDEED empty
        self.assertEqual(output, '', msg="Output is not empty")

    def test_only_invalid_chars_result_in_empty_output(self):
        print(inspect.stack()[0][3])

        fake_file_path="/fake/file/path"
        lines = ["%.,", ",,", "   ", " \" "]  # the last empty line ensures that we have a final '\n'
        fake_file = io.StringIO('\n'.join(lines))

        # Execute main and be sure you capture the output but use mocking to fake a file read by the program
        with io.StringIO() as buf, redirect_stdout(buf):
            with patch('word_index.open', return_value=fake_file, create=True):
                wi_main(fake_file_path)

            output = buf.getvalue()

        # Check the output is not None
        self.assertIsNotNone(output, msg="Output cannot be None")

        # Check the output is empty
        self.assertEqual(output, '', msg="Output is not empty")

    def test_invalid_chars_are_removed(self):
        print(inspect.stack()[0][3])

        fake_file_path="/fake/file/path"
        lines = ["%.,", ",,", "alpha", " \" "]  # the last empty line ensures that we have a final '\n'
        fake_file = io.StringIO('\n'.join(lines))

        # Execute main and be sure you capture the output but use mocking to fake a file read by the program
        with io.StringIO() as buf, redirect_stdout(buf):
            with patch('word_index.open', return_value=fake_file, create=True):
                wi_main(fake_file_path)

            output = buf.getvalue()

        output_lines = list(filter(None, output.split('\n'))) # Split over '\n' but remove empty strings
        expected_n_lines = 1
        expected_output_string = "alpha - 1\n"

        self.assertEqual(expected_n_lines, len(output_lines),
                         msg="Output has wrong number of lines")
        self.assertEqual(expected_output_string, output, msg="Wrong output")


if __name__ == '__main__':
    unittest.main()


