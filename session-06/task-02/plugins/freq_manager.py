class WordFrequencyManager():

    def __init__(self):
        self._word_freqs = {}

    def increment_count(self, word, page):
        if word in self._word_freqs:
            self._word_freqs[word][1].append(page)
            self._word_freqs[word] = \
                (self._word_freqs[word][0] + 1,
                 # Avoid duplicates
                 list(set(self._word_freqs[word][1])))
        else:
            self._word_freqs[word] = (1, [page])

    def filter_and_sort(self, limit):
        # Filtering by frequency
        self._word_freqs = {k: v for k, v in self._word_freqs.items()
                            if v[0] <= limit} # ??
        # Sorting
        return sorted(self._word_freqs.items())
