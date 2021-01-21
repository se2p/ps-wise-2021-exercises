#!/usr/bin/env python

import sys

from monads import TFQuarantine

# The Quarantine Style Description:
# This style is a variation of "The One" Style, with the following additional constraints:
# 
# - Core program functions have no side effects of any kind, including IO
# 
# - All IO actions must be contained in computation sequences that are
#   clearly separated from the pure functions
# 
# - All sequences that have IO must be called from the main program
# 
#


# The functions
#
def get_input(arg):

    # H.O. Function to encapsulate IO
    def _f():
        # This "simulates" the access to an external input. We need this to maintain testing consistent
        # This could be also replaced by a code that reads from stdInput provided we can mock
        # that
        global FILE_LOCATION_IO
        # return sys.argv[1]
        return FILE_LOCATION_IO

    return _f


def extract_lines(path_to_file):
    """
        Takes a path to a file and assigns the entire
        contents of the file to the global variable data.
        A cell is a char. New line chars are included

        Replaces all nonalphanumeric chars in data with white space. But preserve new lines (\n)

        Scans data for lines, filling the global variable line. Note: preserve empty lines !
    """
    def _f():

        with open(path_to_file) as f:
            data = list(f.read())
        # TODO Can't we simply split over lines are then replace nonalphanumeric with spaces?
        data = [c.lower() if c.isalnum() or c == '\n' else ' ' for c in data]
        data_str = ''.join(data)
        lines = data_str.split('\n')
        return lines

    return _f


def index_words(lines):
    """
    Index the words by page
    """
    page_size = 45

    current_line = 1
    current_page = 1
    word_index = []

    for line in lines:

        if current_line > page_size:
            current_line = 1
            current_page += 1

        words = line.split()

        # Since we kept empty lines we need to handle them somehow
        if len(words) > 0:
            for word in words:
                keys = [wd[0] for wd in word_index]
                if word in keys:
                    word_index[keys.index(word)][1].append(current_page)
                else:
                    word_index.append([word, [current_page]])

        current_line +=1

    return word_index


# Note the order of the arguments...
def filter_too_frequent_words(word_index):
    """
    Remove the ones which appear too frequently. Return a copy of the input !
    """
    frequency_threshold = 100
    return [entry for entry in word_index if len(entry[1]) <= frequency_threshold]


def reduce(word_index):
    """
    Remove duplicate pages for terms which appear more than once in the same page. Return a copy of the input !
    """
    return [[entry[0], sorted(set(entry[1]))]for entry in word_index ]


def sort_alphabetically(word_index):
    """
    Sorts word_index alphabetically
    Note: sorted() returns a new sorted list, leaving the original list unaffected
    """
    return sorted(word_index, key=lambda x: str(x[0]), reverse=False)


# Question: this is pure
def pretty_print(word_index):
    """
    Build a string to pretty print the word index
    """
    if len(word_index) == 0:
        return None

    result = ""
    for index, tf in enumerate(word_index):
        result += ' '.join([tf[0], '-', str(tf[1])[1:-1]])
        # Avoid to print a final empty line
        if index + 1 < len(word_index):
            result += '\n'

    return result



def main(file_path):
    # Set the value of the global variable to simulate an
    #   "unsafe" access to Input

    # Note that there's no input provided to the composition, it's just a composition of function.
    # Q: So where's the input comes from?
    global FILE_LOCATION_IO
    FILE_LOCATION_IO = file_path

    #
    # The main function
    #
    TFQuarantine(get_input) \
        .bind(extract_lines) \
        .bind(index_words) \
        .bind(filter_too_frequent_words) \
        .bind(reduce) \
        .bind(sort_alphabetically) \
        .bind(pretty_print) \
        .execute()


if __name__ == "__main__":
    # Note that there should be no input, i.e., sys.argv[1], but this makes testing the program tricky.
    # so we simulate an "UNSAFE access to IO using a global varible"
    main(sys.argv[1])