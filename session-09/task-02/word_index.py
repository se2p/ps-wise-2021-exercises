#!/usr/bin/env python
import sys, queue, threading

#
# The Dataspaces Style Description:
#
# - Existence of one or more units that execute concurrently
# 
# - Existence of one or more data spaces where concurrent units store and
#   retrieve data
# 
# - No direct data exchanges between the concurrent units, other than via the data spaces
#

# Two data spaces implemented as "Global variables"
word_freq_page_map = {}
tuple_space_word_page = queue.Queue()


# Constants
PAGE_SIZE = 45
FREQUENCY_THRESHOLD = 100

PARALLELISM_LEVEL = 5

def fill_dataspaces(path_to_file):

    global word_freq_page_map
    global tuple_space_word_page

    data_str = []

    with open(path_to_file) as f:
        data = f.read()
    # Go over char by char. Preserve new lines
    for i in range(len(data)):
        if (not data[i].isalnum()) and ('\n' != data[i]):
            data_str.append(' ')
        else:
            data_str.append(data[i].lower())

    lines = ''.join(data_str).split('\n')

    for line_number, line in enumerate(lines):
        for word in line.split():
            word_freq_page_map[word] = queue.Queue()
            word_freq_page_map[word].put((0, []))

            # Line_number start from zero ! page number must start from one !
            page = int(line_number / PAGE_SIZE) + 1
            tuple_space_word_page.put([word, page])


def process_words():

    # Get a ref to the "globale" dataspaces
    global word_freq_page_map
    global tuple_space_word_page

    # Homework: Change the condition of the while loop to exit when no more tuples can be find in the dataspace
    while True:
        try:
            # Get the entry from the queue (see the timeout here)
            word_page = tuple_space_word_page.get(timeout=1)

            # Get the corresponding entry from the map
            freq_page_queue = word_freq_page_map[word_page[0]]

            # This is blocking if the entry is empty
            freq_page = freq_page_queue.get()
            freq_page[1].append(word_page[1])
            # Update the entry from the map
            updated_freq_page = (freq_page[0] + 1, list(set(freq_page[1])))

            # Put the entry back into the map (no need to use a different dataspace everytime...)
            word_freq_page_map[word_page[0]].put(updated_freq_page)
        except queue.Empty:
            break


def main(file_path):

    global word_freq_page_map
    global tuple_space_word_page

    # Re-Initialize the global variables to avoid polluting the state of the apps during testing
    word_freq_page_map = {}
    tuple_space_word_page = queue.Queue()

    # Load all the data into the first dataspace. No need to parallelize everything, just make sure threads
    #   never communicate directly
    fill_dataspaces(file_path)

    # Creare the workers. They will execute the process_words function.
    workers = []
    for i in range(PARALLELISM_LEVEL):
        workers.append(threading.Thread(target=process_words))

    # Start all the worker and wait for them to finish.
    # They will load words from one dataspace and put it into a (possibly different) dataspace
    [t.start() for t in workers]
    [t.join() for t in workers]

    # Main prints out the results. Once again, no need to parallelize everything, and no direct communication
    #   between threads
    for sorted_word in sorted(word_freq_page_map.keys(), reverse=False):
        elem = word_freq_page_map[sorted_word].get()
        if elem[0] < FREQUENCY_THRESHOLD:
            print(sorted_word, '-', str(elem[1])[1:-1])


if __name__ == "__main__":
    main(sys.argv[1])

