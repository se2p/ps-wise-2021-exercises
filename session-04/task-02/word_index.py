#!/usr/bin/env python
import sys
import operator

#
# The Bulletin Board Style Description:
#
# - Larger problem is decomposed into entities using some form of abstraction
#   (objects, modules or similar)
# 
# - The entities are never called on directly for actions
# 
# - Existence of an infrastructure for publishing and subscribing to
#   events, aka the bulletin board
# 
# - Entities post event subscriptions (aka 'wanted') to the bulletin
#   board and publish events (aka 'offered') to the bulletin board. the
#   bulletin board does all the event management and distribution#
#

#
# The event management substrate. This is taken from the book by C. V. Lopez
#
class EventManager:

    def __init__(self):
        self._subscriptions = {}

    def subscribe(self, event_type, handler):
        if event_type in self._subscriptions:
            self._subscriptions[event_type].append(handler)
        else:
            self._subscriptions[event_type] = [handler]

    def publish(self, event):
        event_type = event[0]
        if event_type in self._subscriptions:
            for h in self._subscriptions[event_type]:
                h(event)


class DataStorageManager:
    """ Generate 'tagged word' events """

    def __init__(self, event_manager):
        self._data = []

        self._event_manager = event_manager
        self._event_manager.subscribe('load', self.__load )
        self._event_manager.subscribe('start', self.__produce_tagged_words)


    # Load the file content into an array of "lines"
    def __load(self, event):
        # event[0] is the type of event
        path_to_file = event[1]
        _data_str = []

        with open(path_to_file) as f:
            _data = f.read()

        for i in range(len(_data)):
            if (not _data[i].isalnum()) and ('\n' != _data[i]):
                _data_str.append(' ')
            else:
                _data_str.append(_data[i].lower())

        self._data = ''.join(_data_str).split('\n')

    def __produce_tagged_words(self, event):
        for line_number, line in enumerate(self._data):
            for word in line.split():
                self._event_manager.publish(('tagged_word', line_number, word))
        # This notified that we can go on and compute the filtered words
        self._event_manager.publish(('eof', None))


class WordIndexManager:

    def __init__(self, event_manager):
        self._words_and_pages = {}
        self._word_freqs = {}

        # Q1: Can we replace those with a configuration provider that triggers 'configure' events?
        # How can we ensure the correct "global" order when we run the main method?
        self._frequency_threshold = 100
        self._page_size = 45

        self._event_manager = event_manager
        self._event_manager.subscribe('eof', self.__produce_tagged_filtered_sorted_words)
        # Q2: If this component subscribes twice, will it receive the event twice?
        self._event_manager.subscribe('tagged_word', self._do_all)

    def _do_all(self, event):
        line_number = event[1]
        word = event[2]
        # Calling private methods on this/self is ALLOWED
        self.__increment_count(word)
        self.__index_word(line_number, word)

    def __increment_count(self, word):
        if word in self._word_freqs:
            self._word_freqs[word] += 1
        else:
            self._word_freqs[word] = 1

    def _filter(self):
        # Home exercise: replace the following code with a one-liner that removes the elements from the
        #   dictionary while iterating its keys
        _filtered_word_freqs = {}
        for word in self._word_freqs.keys():
            if self._word_freqs[word] <= self._frequency_threshold:
                _filtered_word_freqs[word] = self._word_freqs[word]

        self._word_freqs = _filtered_word_freqs

    def __index_word(self, line_numer, word):
        # Line_number start from zero ! page number must start from one !
        page_number = int(line_numer / self._page_size) + 1

        if word not in self._words_and_pages.keys():
            self._words_and_pages[word] = []

        if page_number not in self._words_and_pages[word]:
            self._words_and_pages[word].append(page_number)

    def __produce_tagged_filtered_sorted_words(self, event):
        # Filter the words by frequency
        self._filter()

        # Sort the filtered words and iterate over them
        for entry in sorted(self._word_freqs.items(), key=operator.itemgetter(0), reverse=False):
            self._event_manager.publish(('filtered_word', entry[0], self._words_and_pages[entry[0]]))

        # This notifies that we can go on and print the words
        self._event_manager.publish(('end', None))


class WordPrinter:

    def __init__(self, event_manager):
        self._word_index = {}

        self._event_manager = event_manager

        self._event_manager.subscribe('filtered_word', self.__accumulate)
        self._event_manager.subscribe('end', self._print_all)

    def __accumulate(self, event):
        word = event[1]
        pages = event[2]
        self._word_index[word]= pages

    def _print_all(self, event):
        for entry in sorted(self._word_index.items(), key=operator.itemgetter(0), reverse=False):
            print(entry[0], '-', str(entry[1])[1:-1])


class WordIndexFramework:

    def __init__(self, event_manager):
        self._event_manager = event_manager
        self._event_manager.subscribe('run', self.run)

    def run(self, event):
        path_to_file = event[1]

        # Note that this is *sync*, so this call returns ONLY after ALL
        #   the registered components have finished to handle the load message
        self._event_manager.publish(('load', path_to_file))
        self._event_manager.publish(('start', None))


#
# The main function
#
def main(path_to_file):
    em = EventManager()
    #

    # Dependency Injection
    DataStorageManager(em)
    WordIndexManager(em)
    WordPrinter(em)
    WordIndexFramework(em)

    # This is sync
    em.publish(('run', path_to_file))


if __name__ == "__main__":
    main(sys.argv[1])