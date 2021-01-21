#!/usr/bin/env python
#!/usr/bin/env python
import sys

from monads import TheOne

#
# The One Description:
#
# - Existence of an abstraction to which values can be
# converted. 
# 
# - This abstraction provides operations to (1) wrap
#   around values, so that they become the abstraction; (2) bind
#   itself to functions, so to establish sequences of functions;
#   and (3) unwrap the value, so to examine the final result.
# 
# - Larger problem is solved as a pipeline of functions bound
#   together, with unwrapping happening at the end.
# 
# - Particularly for The One style, the bind operation simply
#   calls the given function, giving it the value that it holds, and holds
#   on to the returned value.
#

# Global configurations - accessed via function

PAGE_SIZE = 45
FREQUENCY_THRESHOLD = 100


def get_page_size():
    return 45


def get_frequency_threshold():
    return 100



#
# The functions (From the PIPELINE solution)
#
def read_file(path_to_file):
    """
    Takes a path to a file and assigns the entire
    contents of the file to the global variable data.
    A cell is a char. New line chars are included
    """

    with open(path_to_file) as f:
        data = list(f.read())
    return data


def filter_chars_and_normalize(data):
    """
    Replaces all nonalphanumeric chars in data with white space. But preserve new lines (\n), this might not work with \r\m?
    """
    return [c.lower() if c.isalnum() or c == '\n' else ' ' for c in data ]


def scan_lines(data):
    """
    Scans data for lines, filling the global variable line. Note: preserve empty lines !
    """
    data_str = ''.join(data)
    lines = data_str.split('\n')
    return lines


def index_words(lines):
    """
    Index the words by page
    """
    current_line = 1
    current_page = 1
    word_index = []

    for line in lines:

        if current_line > PAGE_SIZE:
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


def filter_too_frequent_words(word_index):
    """
    Remove the ones which appear too frequently. Return a copy of the input !
    """
    return [entry for entry in word_index if len(entry[1]) <= FREQUENCY_THRESHOLD]


def reduce(word_index):
    """
    Remove duplicate pages for terms which appear more than once in the same page. Return a copy of the input !
    """
    return [[entry[0], sorted(set(entry[1])) ]for entry in word_index]


def sort_alphabetically(word_index):
    """
    Sorts word_index alphabetically
    Note: sorted() returns a new sorted list, leaving the original list unaffected
    """
    return sorted(word_index, key=lambda x: str(x[0]), reverse=False)


# TODO? Cannot print an empty line...
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

    # This monads shows how to "fake" imperative programs inside functional ones.
    # The composition is done in the same order of calling bind

    TheOne(file_path)\
        .bind(read_file) \
        .bind(filter_chars_and_normalize) \
        .bind(scan_lines) \
        .bind(index_words) \
        .bind(filter_too_frequent_words) \
        .bind(reduce) \
        .bind(sort_alphabetically) \
        .bind(pretty_print) \
        .print_me()


# https://developer.ibm.com/languages/python/articles/l-prog/

if __name__ == "__main__":
    main(sys.argv[1])
