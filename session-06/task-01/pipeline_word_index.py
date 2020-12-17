#!/usr/bin/env python
import sys, string

# Program Description:
#
# Word Index is a program that takes a plain text file as input and
# outputs all the words contained in it
# sorted alphabetically along with the page numbers on which they occur.
# The program assumes that a page is a
# sequence of 45 lines, each line has max 80 characters, and there is no
# hyphenation. Additionally, Word Index
# must ignore all words that occur more than 100 times.


# Pipeline Style Description:
#   - Larger problem decomposed in functional abstractions.
#       Functions, according to Mathematics, are relations from inputs to outputs.
#   - Larger problem solved as a pipeline of function applications

# Global Constants:
#   Q1: Do the constants violate the style?
LINES_PER_PAGE = 45
MAX_SIZE_LINE = 80
STOP_FREQUENCY_LIMIT = 100


def read_file(path_to_file):
    """ Read data from file as list of characters """
    # Q: Is this function idempotent?
    # Q: Is this function pure?
    data = []
    with open(path_to_file) as f:
        data = data + list(f.read())
    return data


def filter_chars_and_normalize(data):
    """
    Replace non alphanumneric chars with spaces
    """
    return [c.lower() if c.isalnum() or c == '\n' else ' ' for c in data]


def scan(data):
    lines = []
    data_str = ''.join(data)
    lines = lines + data_str.split('\n')
    return lines


def frequencies(lines):
    word_freqs = []
    line_index = 0
    current_page = 0
    for line in lines:
        if line_index % LINES_PER_PAGE == 0:
            current_page += 1
        for w in line.split():
            keys = [wd[0] for wd in word_freqs]
            if w in keys:
                word_freqs[keys.index(w)][1] += 1
                if current_page not in word_freqs[keys.index(w)][2]:
                    word_freqs[keys.index(w)][2].append(current_page)
            else:
                word_freqs.append([w, 1, [current_page]])
        line_index += 1
    return word_freqs


def filter_by_frequency(word_freqs):
    # Q: Is there some other pythonic way to implement this?
    # Q: How can we get rid of "STOP_FREQUENCY_LIMIT"?
    return filter(lambda x: x[1] < STOP_FREQUENCY_LIMIT, word_freqs)


def sort(word_freqs):
    return sorted(list(word_freqs), key=lambda x: x[0], reverse=False)


def print_words(word_freqs):
    for tf in word_freqs:
        print(tf[0], '-', str(tf[2])[1:-1])


def main(file_path):

    # Q: Does the following code violate the style?
    # Piping
    data = read_file(file_path)
    data = filter_chars_and_normalize(data)
    words = scan(data)
    word_freqs = frequencies(words)
    word_freqs = filter_by_frequency(word_freqs)
    word_freqs = sort(word_freqs)
    print_words(word_freqs)


if __name__ == "__main__":
    main(sys.argv[1])