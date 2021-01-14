#!/usr/bin/env python
import sys
#
# The Infinite Mirror Style Description:
#
# - All, or a significant part, of the problem is modelled by
#   induction. That is, specify the base case (n_0) and then the n+1
#   rule
#
#

# NOTE: there's no need for implementing everything as a functions here
# since any abstraction would be fine. However, in as many point as possible we
# need to use recursion

#
# The functions
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
    Replaces all non-alphanumeric chars in data with white space. But preserve new lines (\n). Note: this might not work with \r\n.
    """
    return [c.lower() if c.isalnum() or c == '\n' else ' ' for c in data]


def scan_lines(data):
    """
    Scans data for lines, filling the global variable line.
    Note: preserve empty lines as they count for making pages
    """
    data_str = ''.join(data)
    lines = data_str.split('\n')
    return lines


def _process_lines_in_a_page(current_page, lines, word_index):

    if len(lines) == 0:
        # Base case
        return word_index
    else:
        # Iteration step
        line = lines[0]
        words = line.split()

        # Since we kept empty lines we need to handle them somehow
        if len(words) > 0:
            for word in words:
                keys = [wd[0] for wd in word_index]
                if word in keys:
                    word_index[keys.index(word)][1].append(current_page)
                else:
                    word_index.append([word, [current_page]])

        # Re-invoke itself on the tail of the list
        return _process_lines_in_a_page(current_page, lines[1:])


def index_words(lines, page_size, word_index):
    """
        This function is not recursive, but _process_lines_in_a_page is
    """
    current_page = 1
    # Split the entire works in one-page chunks
    for i in range(0, len(lines), page_size):
        # This is the recursive call which processes chunks of page_size lines at
        #   the time
        _process_lines_in_a_page(current_page, lines[i:i+page_size], word_index)
        #
        current_page = current_page + 1
    return word_index


def filter_too_frequent_words(word_index, frequency_threshold):
    """
    Remove the words which appear too frequently.
    """
    return [entry for entry in word_index if len(entry[1]) <= frequency_threshold]


def remove_duplicate(word_index):
    """
    Remove duplicate pages for terms that appear more than once on the same page.
    """
    return [[entry[0], sorted(set(entry[1]))]for entry in word_index ]


def sort_alphabetically(word_index):
    """
    Sorts word_index by frequency.
    """
    return sorted(word_index, key=lambda x: x[0], reverse=False)


def pretty_print(word_index):
    """
    Pretty print the word index
    """
    if len(word_index) == 0:
        # The following code shows the bottom of the stack, so it's deepest state
        # sys.stderr.write(str(pretty_print.__name__) + ": How big is the stack at this point? " +
        #                  str(len(inspect.stack())) + "\n")
        return
    else:
        tf = word_index[0]
        print(tf[0], '-', str(tf[1])[1:-1])
        # As before we reapply this function to the tail of the list
        pretty_print(word_index[1:])


def main(file_path):
    data = read_file(file_path)
    filtered_and_normalized = filter_chars_and_normalize(data)
    lines = scan_lines(filtered_and_normalized)

    # Example of recursion: Fill up word_index.
    word_index = []
    indexed = index_words(lines, 45, word_index)

    filtered_words = filter_too_frequent_words(indexed, 100)
    reduced_words = remove_duplicate(filtered_words)
    sorted_words = sort_alphabetically(reduced_words)

    # Example of recursion: Print all the data
    pretty_print(sorted_words)
    # Q: Is pretty_print "safe"?
    # Q: What if word_index is really, really large?



if __name__ == "__main__":
    main(sys.argv[1])