#!/usr/bin/env python
import sys

# Monolithic Style Description:
#
#  - No abstractions (do not define classes, modules, or method and functions)
#  - No use of library functions (Let's start with no USER-DEFINED)
#
#
# Global Constants:
#   Q1: Can those be considered as abstractions? Of which type?
#   Q2: Do they violate the Monolithic style?
# LINES_PER_PAGE = 45
# MAX_SIZE_LINE = 80
# STOP_FREQUENCY_LIMIT = 100


# Q3: Defining the main method ease testing, but does this count as violation of
# the style?
def main(file_path,
         LINES_PER_PAGE = 45,
         MAX_SIZE_LINE = 80,
         STOP_FREQUENCY_LIMIT = 100):

    # NOTE: we need to reset the value of all the variables because the unit tests do not restart the interpreter

    # This contains the words that appear more than STOP_FREQUENCY_LIMIT times in the text.
    # Q4: Maybe a set instead of list would have been a better choice?
    stop_words = []

    # The index that contains the words and the pages on which they appear.
    # The idea is to store in the list 'data' objects (i.e., tuples) with the following content:
    # data[0]:  - Word
    # data[1]:  - Frequency
    # data[2]:  - list of Page Numbers (without duplicate entries)
    word_index = []

    # We adopt an approach similar to C. Lopes:
    # 1 - we iterate the file line by line
    # 2 -     while doing this we keep track on which page (and line)
    #               we currently are and parse each word
    # 3 -     when we parse a new word we store the page on which it
    #               appears and increment its frequency
    # 4 -         if a word appears more than a number of time, it becomes
    #               automatically a stop word and must be eliminated/filtered out
    # 5 - Before printing we sort words alphabetically (all the words are normalized lowercase)

    line_index = 0
    current_page = 0

    with open(file_path, 'r') as f:

        for line in f:
            # Q5: The line above could have been implemented as:
            #   "for line_index, line in enumerate(f)"
            # Would have that violated the style? Why?

            # If the line is non-terminated we will miss the last word...
            if not line.endswith("\n"):
                line += "\n"

            # Compute the current page using the line_index. Pages START from 1
            if line_index % LINES_PER_PAGE == 0:
                current_page += 1

            # Parse the words and update the various data structures.
            # This code is similar to the one implementing the WordFrequency program

            start_char = None
            i = 0
            for c in line:

                if start_char is None:
                    if c.isalnum():
                        # We found the start of a word
                        start_char = i
                else:
                    if not c.isalnum():
                        # We found the end of a word. Process it
                        word = line[start_char:i].lower()

                        found = False

                        # Ignore stop words:
                        # Q6: Can the following 'not in' be considered a violation of the style? Why?
                        # What would be an alternative implementation of this check?
                        if word not in stop_words:
                            # Let's see if the word already exists.
                            # Q7: We loop over a COPY of the entire list. Why? Could using slices be considered a
                            #   violation of the style?

                            for data in word_index[:]:
                                # data[0] is the word in lower case
                                if word == data[0]:
                                    found = True
                                    # data[1] is the frequency
                                    data[1] += 1
                                    # Record Page Numbers. This must account for duplicates:
                                    # Q8: Any violations here? What about using a set instead of a list?
                                    if current_page not in data[2]:
                                        data[2].append(current_page)

                                    # Move word from word_index to stop_words
                                    if data[1] > STOP_FREQUENCY_LIMIT:
                                        stop_words.append(word)
                                        word_index.remove(data)

                                    break

                            if not found:
                                data = [word, 1, [current_page]]

                                inserted = False
                                index = 0

                                # Ensure that every new word that we add is in the right place (alphabetic order)
                                while index < len(word_index): # this time we iterate on the actual list and not a copy.
                                    # However, we do not iterate over the values but by index.
                                    if word < word_index[index][0]: # Check: https://thepythonguru.com/python-strings/
                                        # Q9: Does using "string-comparison" count as a violation of the style?
                                        word_index.insert(index, data)
                                        inserted = True
                                        break
                                    index += 1

                                # word is the last word
                                if not inserted:
                                    word_index.append(data)

                        # Let's reset
                        start_char = None

                # Move "line-cursor" forward
                i += 1

            # Move "page-cursor" one line below
            line_index += 1



    for tf in word_index:
        # Q10: Is this ('[1:-1]') a violation? What does it even mean ?!
        print(tf[0], '-', str(tf[2])[1:-1])


if __name__ == "__main__":
    main(sys.argv[1])