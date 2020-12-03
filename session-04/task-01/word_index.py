#!/usr/bin/env python
import operator
import sys

#
# The Hollywood Style Description:
#
# - Larger problem is decomposed into entities using some form of
#       abstraction (objects, modules or similar)
#
# - The entities are never called on directly for ACTIONS (No Action -> No change state)
#       - is_ method
#       - getters
#
# - The entities provide interfaces for other entities to be
#  able to register callbacks
#
# - At certain points of the computation, the entities call on the other
#  entities that have registered for callbacks
#
#


class DataStorageManager:
    """ Generate 'tagged word' events """

    def __init__(self, app):
        self._data = []

        # Q1 Does the order of registration matters?
        self._tagged_word_event_handlers = []

        app.register_for_load_event(self.__load)
        app.register_for_dowork_event(self.__produce_tagged_words)

    # Registration method
    def register_for_tagged_word_event(self, h):
        self._tagged_word_event_handlers.append(h)


    def __load(self, path_to_file):
        """
        Load the file content into an array of "lines"
        """
        _data_str = []

        with open(path_to_file) as f:
            _data = f.read()

        for i in range(len(_data)):
            if (not _data[i].isalnum()) and ('\n' != _data[i]):
                _data_str.append(' ')
            else:
                _data_str.append(_data[i].lower())

        self._data = ''.join(_data_str).split('\n')

    def __produce_tagged_words(self):
        # Home exercise: tag words with pages
        for line_number, line in enumerate(self._data):
            for word in line.split():
                for h in self._tagged_word_event_handlers:
                    h(line_number, word)


class WordsIndexManager:

    def __init__(self, app, tagged_word_producer):
        self._words_and_pages = {}
        self._word_freqs = {}

        # Home Exercise: Encapsulate the configurations into a new component/class
        self._frequency_threshold = 100
        self._page_size = 45

        self._tagged_filtered_word_event_handlers = []

        # WordsIndexManager registers for notifications
        app.register_for_end_event(self.__produce_tagged_filtered_sorted_words)

        # Q1: Why the this component registers two times? What will happen at runtime?
        tagged_word_producer.register_for_tagged_word_event(self.__increment_count)
        tagged_word_producer.register_for_tagged_word_event(self.__index_word)

    def register_for_tagged_filtered_word_event(self, h):
        self._tagged_filtered_word_event_handlers.append(h)

    def __increment_count(self, line_number, word):
        # line_number is discarded but we need the parameter...
        if word in self._word_freqs:
            self._word_freqs[word] += 1
        else:
            self._word_freqs[word] = 1

    # Q2: I implemented filtering inside this class, but I could have defined another abstraction unit.
    # How would I need to change the program to make that work?

    def _filter(self):
        """ Filter the words by frequency """
        _filtered_word_freqs = {}
        for word in self._word_freqs.keys():
            if self._word_freqs[word] <= self._frequency_threshold:
                _filtered_word_freqs[word] = self._word_freqs[word]

        self._word_freqs = _filtered_word_freqs

    def __index_word(self, line_numer, word):
        page_number = int(line_numer / self._page_size) + 1

        if word not in self._words_and_pages.keys():
            self._words_and_pages[word] = []

        if page_number not in self._words_and_pages[word]:
            self._words_and_pages[word].append(page_number)

    def __produce_tagged_filtered_sorted_words(self):

        # Q3: Is this a violation of the style?
        self._filter()

        # iterate over the sorted and filtered words
        for entry in sorted(self._word_freqs.items(), key=operator.itemgetter(0), reverse=False):
            word = entry[0]
            # Return the entry corresponding to the word from the index
            for h in self._tagged_filtered_word_event_handlers:
                h(word, self._words_and_pages[word])


class WordPrinter:

    def __init__(self, words_index_manager):
        words_index_manager.register_for_tagged_filtered_word_event(self.__print_word_and_pages)

    # This assumes that words are already sorted !
    def __print_word_and_pages(self, word, pages):
        print(word, '-', str(pages)[1:-1])


class WordIndexFramework:
    """ Generates configure/setup, load, do_work, and end events """

    # The computation is logically divided in steps:
    # 1 . Load the data
    # 2 . Process data
    # 3 . Print them

    def __init__(self):
        self._load_event_handlers = []
        self._dowork_event_handlers = []
        self._end_event_handlers = []

    def register_for_load_event(self, handler):
        self._load_event_handlers.append(handler)

    def register_for_dowork_event(self, handler):
        self._dowork_event_handlers.append(handler)

    def register_for_end_event(self, handler):
        self._end_event_handlers.append(handler)

    def run(self, path_to_file):
        for h in self._load_event_handlers:
            h(path_to_file)
        for h in self._dowork_event_handlers:
            h()
        for h in self._end_event_handlers:
            h()


#
# The main function
#
def main(path_to_file):
    # Instantiating the components
    wif = WordIndexFramework()

    # Register for LOAD event
    # Register for DO_WORK event -> produces TAGGER_WORD events
    data_storage = DataStorageManager(wif)

    # Register for TAGGED_WORD events -> produces TAGGED_FILTERED_WORD events
    # Register for END events ->
    words_index_manager = WordsIndexManager(wif, data_storage)

    # Register for TAGGED_FILTERED_WORD events
    words_printer = WordPrinter(words_index_manager)

    # Trigger the events
    wif.run(path_to_file)


if __name__ == "__main__":
    main(sys.argv[1])
