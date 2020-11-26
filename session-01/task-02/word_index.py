#!/usr/bin/env python

# Program Description:
#
# Word Index is a program that takes a plain text file as input and
# outputs all the words contained in it sorted alphabetically along
# with the page numbers on which they occur.

# The program assumes that a page is a sequence of 45 lines,
# each line has max 80 characters, and there is no hyphenation.

# Additionally, Word Index must ignore all words that occur more than 100 times.

####################################
# Free Flow, a.k.a. No Style
####################################

import sys, string

# Global "constants"
LINES_PER_PAGE       =  45
MAX_SIZE_LINE        =  80
STOP_FREQUENCY_LIMIT = 100

class WordIndexData:

    def __init__(self, word):
        self.word = word
        self.frequency = 0
        self.pages = set()

    def appear_on(self, page):
        """ Increment frequency of occurrences and store page without duplicates"""
        self.frequency += 1
        self.pages.add(page)


def parse_line(line):
    """ Parse the line and return the list of words found. We assume line is less or equal to 80 chars"""
    start_char = None
    for i, c in enumerate(line):

        if start_char is None:
            if c.isalnum():
                # We found the start of a word
                start_char = i
        else:
            if not c.isalnum():
                # We found the end of a word.
                word = line[start_char:i].lower()
                yield word

                # Let's reset and restart
                start_char = None


def main(file_path):
    word_index = []

    current_page = 0

    # In this case, it is not necessary to append the '\n' at the end of the line
    with open(file_path, 'r') as f:

        for line_number, line in enumerate(f):

            # Compute the current page using the line_index. Pages START from 1
            if line_number % LINES_PER_PAGE == 0:
                current_page += 1

            for word in parse_line(line):
                if word not in [data.word for data in word_index[:]]:
                    data = WordIndexData(word)
                    data.appear_on(current_page)
                    #
                    word_index.append(data)
                else:
                    # Update data
                    [data.appear_on(current_page) for data in word_index if data.word == word]

    # Remove all the words that appeared too often
    # Q: Can you find a more python way to rewrite this code?
    word_index = list(filter(lambda data: data.frequency <= STOP_FREQUENCY_LIMIT, word_index))

    # Sort the word_index by word. This changes the object itself
    word_index.sort(key=lambda x: x.word, reverse=False)

    # Print them
    for data in word_index:
        print(data.word, '-', str(data.pages)[1:-1])


if __name__ == "__main__":
    main(sys.argv[1])