#!/usr/bin/env python

#
# The Plugins Style Description:
#
# - The problem is decomposed using some form of abstraction
#   (procedures, functions, objects, etc.)
# 
# - All or some of those abstractions are physically encapsulated into
#   their own, usually pre-compiled, packages. Main program and each of
#   the packages are compiled independently. These packages are loaded
#   dynamically by the main program, usually in the beginning (but not
#   necessarily).
# 
# - Main program uses functions/objects from the dynamically-loaded
#   packages, without knowing which exact implementations will be
#   used. New implementations can be used without having to adapt or
#   recompile the main program.
# 
# - External specification of which packages to load. This can be done
#   by a configuration file, path conventions, user input or other
#   mechanisms for external specification of code to be linked at run
#   time.
#
#!/usr/bin/env python
import sys, configparser, importlib.machinery

# Program Description:
#
# Word Index is a program that takes a plain text file as input and
# outputs all the words contained in it
# sorted alphabetically along with the page numbers on which they occur.
# The program assumes that a page is a
# sequence of 45 lines, each line has max 80 characters, and there is no
# hyphenation. Additionally, Word Index
# must ignore all words that occur more than 100 times.

#
# The Plugins Style Description:
#
# - The problem is decomposed using some form of abstraction
#   (procedures, functions, objects, etc.)
#
# - All or some of those abstractions are physically encapsulated into
#   their own, usually pre-compiled, packages. Main program and each of
#   the packages are compiled independently. These packages are loaded
#   dynamically by the main program, usually in the beginning (but not
#   necessarily).
#
# - Main program uses functions/objects from the dynamically-loaded
#   packages, without knowing which exact implementations will be
#   used. New implementations can be used without having to adapt or
#   recompile the main program.
#
# - External specification of which packages to load. This can be done
#   by a configuration file, path conventions, user input or other
#   mechanisms for external specification of code to be linked at run
#   time.
#


class WordIndexController:

    def __init__(self, storage_manager, word_freq_manager):
        self.storage_manager = storage_manager
        self.word_freq_manager = word_freq_manager

    def run(self, page_size, freq_limit):
        while self.storage_manager.has_next_line():
            line_number, words = self.storage_manager.next_line()
            page_number = int(line_number / page_size) + 1
            for word in words:
                self.word_freq_manager.increment_count(word, page_number)

        word_freqs = self.word_freq_manager.filter_and_sort(freq_limit)

        for tf in word_freqs:
            print(tf[0], '-', str(tf[1][1])[1:-1])


def main(path_to_file):
    # Read from the configuration file how to setup plugins
    config = configparser.ConfigParser()
    config.read("config.ini")

    # Load configuration values from the configuration file
    page_size = int(config.get("Configuration", "page_size"))
    freq_limit = int(config.get("Configuration", "freq_limit"))

    # Load the plugins from the files listed in the configuration file
    # Q: Can you extend this by including also the CLASS to load from the module?
    storage_manager_plugin = config.get("Plugins", "storage_manager")
    word_freq_manager_plugin = config.get("Plugins", "word_freq_manager")

    # Load the actual code
    sm = importlib.machinery.SourceFileLoader('storage_manager', storage_manager_plugin).load_module()
    wfm = importlib.machinery.SourceFileLoader('word_freq_manager', word_freq_manager_plugin).load_module()

    # Instantiate the classes now that you imported their modules
    storage_manager = sm.DataStorageManager(path_to_file)
    word_freq_manager = wfm.WordFrequencyManager()

    # Instantiate the local controller
    wic = WordIndexController(storage_manager, word_freq_manager)
    wic.run( page_size, freq_limit)


if __name__ == "__main__":
    main(sys.argv[1])