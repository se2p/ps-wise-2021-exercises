import re

class DataStorageManager():
    """ Models the contents of the file """

    # Cursor. Arrays start at 0 but lines on a page start at 1
    _currentLine = 0

    def __init__(self, path_to_file):
        with open(path_to_file) as f:
            # Q: Is this correct ?
            self._data = f.read()
        self._lines = self._data.split('\n')
        pattern = re.compile('[\W_]+')
        for idx in range(len(self._lines)):
            self._lines[idx] = pattern.sub(' ', self._lines[idx]).lower()

    def has_next_line(self):
        return self._currentLine < len(self._lines) - 1

    def next_line(self):
        """ Return the words in the line or raise an exception """
        self._currentLine += 1
        return self._currentLine, self._lines[self._currentLine - 1].split()