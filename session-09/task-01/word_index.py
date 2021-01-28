#!/usr/bin/env python
import sys, re, operator, string

# Import here the "Actor"
from concurrency import TheActor, send_message
#
# The Actors Style Description:
#
# Similar to the letterbox style, but where the 'things' have
# independent threads of execution.
# 
# - The larger problem is decomposed into 'things' that make sense for
#   the problem domain 
# 
# - Each 'thing' has a queue meant for other \textit{things} to place
#   messages in it
# 
# - Each 'thing' is a capsule of data that exposes only its
#   ability to receive messages via the queue
# 
# - Each 'thing' has its own thread of execution independent of the
#   others.
#


class DataStorageManager(TheActor):
    """ Models the contents of the file and return lines"""

    def _dispatch(self, message):
        if message[0] == 'init':
            self._init(message[1])
        elif message[0] == 'lines':
            self._get_lines(message[1])
        else:
            raise Exception("Message not understood " + message[0])

    def _init(self, path_to_file):
        data_str = []

        with open(path_to_file) as f:
            data = f.read()
        # Go over char by char. Preserve new lines
        for i in range(len(data)):
            if (not data[i].isalnum()) and ('\n' != data[i]):
                data_str.append(' ')
            else:
                data_str.append(data[i].lower())

        self._lines = ''.join(data_str).split('\n')

    def _get_lines(self, recipient):
        """ Returns the list of lines in storage  """
        send_message(recipient, ['lines', self._lines])


class WordFrequencyManager(TheActor):
    """ Keeps the word frequency data, filter them by absolute frequency and return the words sorted upon request """


    def _dispatch(self, message):
        if message[0] == 'init':
            self._init(message[1])
        elif message[0] == 'increment_count':
            self._increment_count(message[1])
        elif message[0] == 'get_words':
            self._get_words(message[1])
        else:
            raise Exception("Message not understood " + message[0])

    def _init(self, frequency_threshold):
        self._word_freqs = {}
        self._frequency_threshold = frequency_threshold

    def _increment_count(self, word):
        if word in self._word_freqs:
            self._word_freqs[word] += 1
        else:
            self._word_freqs[word] = 1

    def _get_words(self, recipient):

        # Filter
        _filtered_word_freqs = {}
        for word in self._word_freqs.keys():
            if self._word_freqs[word] <= self._frequency_threshold:
                _filtered_word_freqs[word] = self._word_freqs[word]
        self._word_freqs = _filtered_word_freqs

        # Sort and send. TODO Really necessary?
        # Assume the medium will deliver words in order
        words = [entry[0] for entry in sorted(self._word_freqs.items(), key=operator.itemgetter(0), reverse=False)]
        send_message(recipient, ['words', words])


class WordsIndexer(TheActor):

    def _dispatch(self, message):
        if message[0] == 'init':
            self._init(message[1])
        elif message[0] == 'index_word':
            self._index_word(message[1], message[2])
        elif message[0] == 'get_pages_for_word':
            self._get_pages_for_word(message[1], message[2])
        elif message[0] == 'eof':
            self._eof(message[1])
        else:
            raise Exception("Message not understood " + message[0])

    def _init(self, page_size):
        self._words_and_pages = {}
        self._page_size = page_size

    def _index_word(self, word, line_numer):
        # Line_number start from zero ! page number must start from one !
        page_number = int(line_numer / self._page_size) + 1

        if word not in self._words_and_pages.keys():
            self._words_and_pages[word] = []

        if page_number not in self._words_and_pages[word]:
            self._words_and_pages[word].append(page_number)

    def _get_pages_for_word(self, recipient, word):
        if word in self._words_and_pages.keys():
            send_message(recipient, ['pages_for_word', word, self._words_and_pages[word]])

    def _eof(self, recipient):
        send_message(recipient, ['eof'])


class WordIndexController(TheActor):

    def _dispatch(self, message):
        if message[0] == 'init':
            self._init(message[1:])
        elif message[0] == 'run':
            self._run()
        elif message[0] == 'lines':
            self._process_lines(message[1])
        elif message[0] == 'words':
            self._get_pages(message[1])
        elif message[0] == 'pages_for_word':
            self._print_pages(message[1], message[2])
        elif message[0] == 'eof':
            self._done()
        else:
            raise Exception("Message not understood " + message[0])

    def _init(self, message):
        self.storage_manager = message[0]
        self.word_freq_manager = message[1]
        self.word_indexer = message[2]

    def _process_lines(self, lines):
        for line_number, line in enumerate(lines):
            for w in line.split():
                send_message(self.word_freq_manager, ['increment_count',w])
                send_message(self.word_indexer, ['index_word', w, line_number])

        # Question: At this point we assume that word_freq_manager processed already all the words
        #   but how one can be sure about that?
        send_message(self.word_freq_manager, ['get_words', self])

    def _get_pages(self, words):
        self.words = words
        # self.count = len(words)
        # Tell word_indexer to get you back the pages corresponding to each word
        [send_message(self.word_indexer, ['get_pages_for_word', self, word]) for word in words]
        # Force and "EOF" here? or die ?
        send_message(self.word_indexer, ['eof', self])

    # Assuming those arrives in order, we can print them on the fly
    def _print_pages(self, word, pages_for_word):
        # TODO Extract the word and the page or synch using words?
        print(word, '-', str(pages_for_word)[1:-1])  # [1:-1] removes the parentheses ?
        # Remove word from self.words
        # self.words.remove(word)
        # Replaced by EOF
        # self.count -= 1
        # if self.count == 0:
        #     self._done()

    def _done(self):
        for recipient in [self.storage_manager, self.word_freq_manager, self.word_indexer, self]:
            send_message(recipient, ['die'])
        # Alternatively we could have used:
        # self._stopMe = True

    def _run(self):
        send_message(self.storage_manager, ['lines', self])


#
# The main function
#
PAGE_SIZE=45
FREQUENCY_THRESHOLD=100


def main(file_path):
    #
    # Instantiation and start all the actors
    # - No Args constructor to separate instantiation and initialization
    #
    storage_manager = DataStorageManager()
    word_freq_manager = WordFrequencyManager()
    word_indexer = WordsIndexer()
    word_index_controller = WordIndexController()

    #
    # Initialization and wiring (ref of an actor passed to another one)
    #
    send_message(storage_manager, ['init', file_path])
    send_message(word_freq_manager, ['init', FREQUENCY_THRESHOLD])
    send_message(word_indexer, ['init', PAGE_SIZE])
    # Passing references to other actors is not a violation. BUT DIRECTLY CALLING METHODS OF THE ACTORS IS!
    send_message(word_index_controller, ['init', storage_manager, word_freq_manager, word_indexer])

    # Start the execution
    send_message(word_index_controller, ['run'])

    # At this point we need to "block" main thread and wait for the all the actors to finish
    [t.join() for t in [storage_manager, word_freq_manager, word_indexer, word_index_controller]]


if __name__ == "__main__":
    main(sys.argv[1])