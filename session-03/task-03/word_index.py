#!/usr/bin/env python
import sys, re

# Q1 In the book, C. V. Lopez uses Abstract Classes, can you rework this solution to make use of them as well?
# from abc import ABCMeta

# Letterbox Style Description:
#
# - The larger problem is decomposed into 'things' that make sense for
#   the problem domain
#
# - Each 'thing' is a capsule of data that exposes one single procedure (dispatch),
#   namely the ability to receive and dispatch messages that are sent to
#   it
#
# - Message dispatch can result in sending the message to another capsule


class DataStorageManager:

    def dispatch(self, message):
        if message[0] == 'init':
            self._init(message[1])
        elif message[0] == 'has_next_line':
            return self._has_next_line()
        elif message[0] == 'next_line':
            return self._next_line()
        else:
            # Q1: What's the problem with this code?
            print("Cannot understand your message")

    # Q2: All the methods are "private" isn't this a violation of the style?
    def _init(self, path_to_file):
        self._currentLine = 0
        with open(path_to_file) as f:
            self._data = f.read()
        self._lines = self._data.split('\n')
        pattern = re.compile('[\W_]+')
        for idx in range(len(self._lines)):
            self._lines[idx] = pattern.sub(' ', self._lines[idx]).lower()

    def _has_next_line(self):
        return self._currentLine < len(self._lines) - 1

    def _next_line(self):
        self._currentLine += 1
        return self._currentLine, self._lines[self._currentLine - 1].split()


class WordFilter:

    def dispatch(self, message):
        if message[0] == 'filter_by_frequency':
            return self._filter_by_frequency(message[2])
        else:
            print("Cannot understand your message")

    def _filter_by_frequency(self, word_freq):
        return {k: v for k, v in word_freq.items() if v[0] <= 100}


class WordFrequencyManager:

    def dispatch(self, message):
        if message[0] == 'init':
            return self._init()
        elif message[0] == 'increment_count':
            return self._increment_count(message[1], message[2])
        elif message[0] == 'filter_and_sort':
            return self._filter_and_sort()
        else:
            print("Cannot understand your message")

    def _init(self):
        self._word_freqs = {}
        self._word_filter = WordFilter()

    def _increment_count(self, word, page):
        if word in self._word_freqs:
            self._word_freqs[word][1].append(page)
            self._word_freqs[word] = (self._word_freqs[word][0] + 1, list(set(self._word_freqs[word][1])))
        else:
            self._word_freqs[word] = (1, [page])

    def _filter_and_sort(self):
        filtered_dict = self._word_filter.dispatch(['filter_by_frequency', self._word_freqs])
        return sorted(filtered_dict.items())


class WordFrequencyController:

    # THE CODE IS ONLY FOR DISPATCHING
    def dispatch(self, message):
        if message[0] == 'init':
            self._init(message[1])
        elif message[0] == 'run':
            self._run()
        else:
            print("Cannot understand your message")




    def _init(self, path_to_file):
        self._storage_manager = DataStorageManager()
        self._storage_manager.dispatch(['init', path_to_file])

        self._word_freq_manager = WordFrequencyManager()
        self._word_freq_manager.dispatch(['init'])

    def _run(self):
        while self._storage_manager.dispatch(['has_next_line']):
            line_number, words = self._storage_manager.dispatch(['next_line'])
            page_number = int(line_number / 45) +1
            for word in words:
                self._word_freq_manager.dispatch(['increment_count', word, page_number])

        word_freqs = self._word_freq_manager.dispatch(['filter_and_sort'])
        for tf in word_freqs:
            print(tf[0], '-', str(tf[1][1])[1:-1])


def main(file_path):
    # INSTANTIATION is SEPARATED FROM INITIALIZATION
    word_frequency_controller = WordFrequencyController()
    #
    word_frequency_controller.dispatch(['init', file_path])
    word_frequency_controller.dispatch(['run'])


if __name__ == "__main__":
    main(sys.argv[1])