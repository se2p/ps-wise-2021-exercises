#!/usr/bin/env python
import sys, re
import os

# The Things Style Description:
#
# - The larger problem is decomposed into 'things' that make sense for
#   the problem domain
#
# - Each 'thing' is a capsule of data that exposes procedures to the
#   rest of the world
#
# - Data is never accessed directly, only through these procedures
#
# - Capsules can reappropriate procedures defined in other capsules

class Configuration:
    _PAGE_SIZE = 45
    _FREQ_LIMIT = 100

    def get_page_size(self):
        return self._PAGE_SIZE

    def get_freq_limit(self):
        return self._FREQ_LIMIT


class DataStorageManager:
    """ Models the contents of the file """

    # Cursor. Arrays start at 0 but lines on a page start at 1
    _currentLine = 0

    pattern = re.compile('[\W_]+')

    def __init__(self, path_to_file):
        with open(path_to_file) as f:
            # Q: Is this correct ?
            self._data = f.read()
        self._lines = self._data.split('\n')
        for idx in range(len(self._lines)):
            self._lines[idx] = self.pattern.sub(' ', self._lines[idx]).lower()

    def has_next_line(self):
        return self._currentLine < len(self._lines) - 1

    def next_line(self):
        """ Return the words in the line or raise an exception """
        self._currentLine += 1
        return self._currentLine, self._lines[self._currentLine - 1].split()


class WordFrequencyManager:

    def __init__(self):
        self._word_freqs = {}

    def increment_count(self, word, page):
        if word in self._word_freqs:
            self._word_freqs[word][1].append(page)
            self._word_freqs[word] = \
                (self._word_freqs[word][0] + 1,
                 # Avoid duplicates
                 list(set(self._word_freqs[word][1])))
        else:
            self._word_freqs[word] = (1, [page])

    def filter_and_sort(self, limit):
        # Filtering by frequency
        self._word_freqs = {k: v for k, v in self._word_freqs.items()
                            if v[0] <= limit} # ??
        # Sorting
        return sorted(self._word_freqs.items())


class WordFrequencyController:

    def __init__(self, path_to_file):
        self._storage_manager = DataStorageManager(path_to_file)
        self._conf = Configuration()
        self._word_freq_manager = WordFrequencyManager()

    def run(self):
        while self._storage_manager.has_next_line():
            line_number, words = self._storage_manager.next_line()
            page_number = int(line_number / self._conf.get_page_size() ) + 1
            for word in words:
                self._word_freq_manager.increment_count(word, page_number)

        word_freqs = self._word_freq_manager.filter_and_sort(self._conf.get_freq_limit())

        for tf in word_freqs:
            print(tf[0], '-', str(tf[1][1])[1:-1])


def main(file_path):
    if os.path.exists(file_path):
        wfc = WordFrequencyController(file_path)
        wfc.run()


if __name__ == "__main__":
    main(sys.argv[1])