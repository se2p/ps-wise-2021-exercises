#!/usr/bin/env python
import sys, re

# Closed-Map Style Description:
#
# - The larger problem is decomposed into 'things' that make sense for
#   the problem domain
#
# - Each 'thing' is a map from keys to values. Some values
#   are procedures/functions.

# The following functions do not fit well as lambdas
def init_data_storage_manager(obj, path_to_file, cfg):
    with open(path_to_file) as f:
        # Q1: Is this a violation of the style? Should we use obj['data'] instead ?
        data = f.read()

    obj['_lines'] = data.split('\n')
    pattern = re.compile('[\W_]+')
    for idx in range(len(obj['_lines'])):
        obj['_lines'][idx] = pattern.sub(' ', obj['_lines'][idx]).lower()
    # Q2: Is this a violation of the style?
    obj['_lines'] = list(filter(lambda x: len(x) > 0, obj['_lines']))
    obj['_configuration'] = cfg

def retrieve_next_line(obj):
    obj['_currentLine'] += 1
    return obj['_lines'][obj['_currentLine'] -1].split()


def increment_word_count(obj, word, page):
    if word in obj['_word_freqs']:
        obj['_word_freqs'][word] = (obj['_word_freqs'][word][0] + 1, obj['_word_freqs'][word][1])
        # Avoid duplicates
        if page not in obj['_word_freqs'][word][1]:
            obj['_word_freqs'][word][1].append(page)
    else:
        obj['_word_freqs'][word] = (1, [page])


def get_filtered_sorted_output(self_obj):
    self_obj['_word_freqs'] = {k: v for k, v in self_obj['_word_freqs'].items() if v[0] <= 100}
    return sorted(self_obj['_word_freqs'].items())







def main(file_path):

    configuration_object = {
        '_page_size' : 45,
        'get_page_size': lambda : configuration_object['_page_size']
    }


    # Q1: Here we manually setup the objects.
    # What would be an alternative way of achieving the same?
    data_storage_manager_object = {
        # Fields declaration
        '_currentLine': 0,
        '_lines': [],

        # THIS IS A VIOLATION
        '_configuration' : None,

        # Methods declaration: here the map CLOSE on itself !
        'init': lambda path_to_file, cfg: init_data_storage_manager(data_storage_manager_object, path_to_file, cfg),
        # Q2: Is this a violation of the style?
        'has_next_line': lambda: data_storage_manager_object['_currentLine'] < len(data_storage_manager_object['_lines']),
        'next_line': lambda: retrieve_next_line(data_storage_manager_object),
        # Q3: Is this a violation of the style
        'line_number': lambda: data_storage_manager_object['_currentLine']
    }
    data_storage_manager_object['init'](file_path)

    word_frequency_manager_object = {
        # Fields declaration
        '_word_freqs': {},
        # Methods declaration.
        # Q4: Why do we need a lambda here? Couldn't we simply store the function object and use it?
        'increment_count': lambda word, page: increment_word_count(word_frequency_manager_object, word, page),
        'filter_and_sort': lambda: get_filtered_sorted_output(word_frequency_manager_object)
    }

    # Q5: Is this a violation of the style?
    # Q6: Can a map store/reference another closed-map?
    while data_storage_manager_object['has_next_line']():
        words = data_storage_manager_object['next_line']()
        line_number = data_storage_manager_object['line_number']()

        for w in words:
            word_frequency_manager_object['increment_count'](w, int(line_number/ 45) + 1)

    word_freqs = word_frequency_manager_object['filter_and_sort']()

    # Q7: Is this a violation of the style?
    for tf in word_freqs:
        print(tf[0], '-', str(tf[1][1])[1:-1])


if __name__ == "__main__":
    main(sys.argv[1])