#!/usr/bin/env python
import sys

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
    # Q1: Is this function idempotent?
    # Q2: Is this function pure?
    data = []
    with open(path_to_file) as f:
        data = data + list(f.read())
    return data


def filter_chars_and_normalize(data):
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


# Q3: Does this function violate the style?
def filter_by_frequency(word_freqs):
    # Q4: How can we get rid of "STOP_FREQUENCY_LIMIT"?
    return [word for word in filter(lambda x: x[1] < STOP_FREQUENCY_LIMIT, word_freqs)]


# Q5: Does this function violate the style?
def sort(word_freqs):
    word_freqs.sort()
    return word_freqs


# Q6: Does this function violate the style?
def print_words(word_freqs):
    for tf in word_freqs:
        print(tf[0], '-', str(tf[2])[1:-1])


def main(file_path ):
    # Q7: Does the following code violate the style?
    data       = read_file(file_path)
    data       = filter_chars_and_normalize(data)
    words      = scan(data)
    word_freqs = frequencies(words)
    word_freqs = filter_by_frequency(word_freqs)
    word_freqs = sort(word_freqs)
    print_words(word_freqs)


if __name__ == "__main__":
    main(sys.argv[1])