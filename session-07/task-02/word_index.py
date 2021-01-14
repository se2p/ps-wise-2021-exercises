#!/usr/bin/env python
import sys
import inspect
from functools import partial
#
# The Kick-forward Style Description:
#
# Variation of the pipeline style, with the following additional constraints:
# 
# - Each function takes an additional parameter, usually the 
#   last, which is another function
# 
# - That function parameter is applied at the end of the current
#   function
# 
# - That function parameter is given as input what would be the
#   output of the current function
# 
# - Larger problem is solved as a pipeline of functions, but where
#   the next function to be applied is given as parameter to the current function
#


# Global configurations: VIOLATION OF STYLES. WE CAN PROBABLY MAKE THEM PRIVATE USING A CLOSURE?
PAGE_SIZE = 45
FREQUENCY_THRESHOLD = 100

#
# The functions
#
def read_file(path_to_file, next_function):
    """
    Takes a path to a file and assigns the entire
    contents of the file to the global variable data.
    A cell is a char. New line chars are included
    """
    __debug_call(next_function)

    with open(path_to_file) as f:
        data = list(f.read())

    # instead of returing the data like pipeline style, we "pass the ball" to the
    # next function. At the same time, we configure the execution to use scal_line as the
    # function after it

    # note: next_function is "filter_chars_and_normalize"
    next_function(data, scan_lines)


def filter_chars_and_normalize(data, next_function):
    """
    Replaces all non-alphanumeric chars in data with white space. But preserve new lines (\n), this might not work with \r\m?
    """
    __debug_call(next_function)

    data = [c.lower() if c.isalnum() or c == '\n' else ' ' for c in data ]
    # next_function is: scan_lines, so the next one must be index_words.
    # but index words takes two parameters: the data nad the page_size... how to solve it?
    #
    #
    #
    # Partial function application...but we should fix the second-left-most parameter, while "partial" allows
    # only the left-most...
    # Q: how can we solve this?
    # SOL1 (not shown): redefine the function by moving the parameters-to-be-fixed in the left-most position
    # SOL2: redefine: redefine the function by moving the parameters-to-be-fixed in the left-most position, on-the-fly
    #
    # However, there's a catch: partial objects are like function objects in that they are callable, weak referencable,
    # and can have attributes. There are some important differences. For instance, the __name__ and __doc__ attributes
    # are not created automatically. Also, partial objects defined in classes behave like static methods and do not
    # transform into bound methods during instance attribute look-up.

    index_words_with_fixed_page_size = partial(
        lambda page_size, data, next_function: index_words(data, page_size, next_function), 45)
    setattr(index_words_with_fixed_page_size, "__name__", "index_words")

    next_function(data, index_words_with_fixed_page_size)


def scan_lines(data, next_function):
    """
    Scans data for lines, filling the global variable line. Note: preserve empty lines !
    """
    __debug_call(next_function)

    data_str = ''.join(data)
    lines = data_str.split('\n')

    # next_function is: index_words, so then one following it is: filter_too_frequent_words
    next_function(lines, filter_too_frequent_words)


# Exercise: Handle multiple parameters: what to use partial application, currying, or multiple parameters?
def index_words(lines, page_size, next_function):
    """
        Index the words by page
    """
    __debug_call(next_function)

    # page_size = PAGE_SIZE

    current_line = 1
    current_page = 1
    word_index = []

    for line in lines:

        if current_line > page_size:
            current_line = 1
            current_page += 1


        # This is "unsafe" as multiple spaces are considered as separate "empty" words !
        # words = line.strip().split(' ')

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


    # next_function is: filter_too_frequent_words, so the next one is reduce
    next_function(word_index, reduce)



def filter_too_frequent_words(word_index, next_function):
    """
    Remove the ones which appear too frequently. Return a copy of the input !
    """
    __debug_call(next_function)

    frequency_threshold = FREQUENCY_THRESHOLD
    # next_function is: reduce, so the next one is sort_alphabetically
    next_function([entry for entry in word_index if len(entry[1]) <= frequency_threshold], sort_alphabetically)


def reduce(word_index, next_function):
    """
    Remove duplicate pages for terms which appear more than once in the same page. Return a copy of the input !
    """

    __debug_call(next_function)

    # next_function is sort_alphabetically, so the one following is pretty_print
    next_function([ [entry[0], sorted(set(entry[1])) ]for entry in word_index ], pretty_print)


def sort_alphabetically(word_index, next_function):
    """
    Sorts word_index by frequency.
    Note: sorted() returns a new sorted list, leaving the original list unaffected
    """
    __debug_call(next_function)

    next_function(sorted(word_index, key=lambda x: x[0], reverse=False), no_op)


def pretty_print(word_index, next_function):
    """
    Pretty print the word index
    """
    __debug_call(next_function)

    for tf in word_index:
        print(tf[0], '-', str(tf[1])[1:-1])

    # This returns void
    next_function(None)


def no_op(next_function):

    __debug_call(next_function)

    # This is superflous
    # return


def main(file_path):
    #
    # We keep the functions from the original pipeline style and adapt them to fit the new style.
    # Below the "original" flow of the functions
    #
    # read_file -> filter_chars_and_normalize
    # filter_chars_and_normalize -> scan_lines
    # scan_lines -> index_words
    # index_words -> filter_too_frequent_words
    # filter_too_frequent_words -> reduce
    # reduce -> sort_alphabetically
    # sort_alphabetically -> pretty_print
    # pretty_print -> (no_op)
    # (no_op) --> This is the end. we return (and end).
    #

    # Decides the function that will process the result of "read_file" and will be called right after it
    next_function = filter_chars_and_normalize
    read_file(file_path, next_function)


def __debug(ret):
    print("%s --> %s (%d)" % ((inspect.stack()[1][3]),
                              ret.__name__ if ret is not None else None,
                              len(inspect.stack())), file = sys.stderr)
    pass

def __skip(ret):
    pass

# TODO Homework: use a decorator or an aspect to add debug information
__debug_call = __skip

if __name__ == "__main__":
    main(sys.argv[1])