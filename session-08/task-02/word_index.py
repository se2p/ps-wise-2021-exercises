#!/usr/bin/env python
#
# The Quarantine Style Description:
# This style is a variation of "The One" Style, with the following additional constraints:
# 
# - Core program functions have no side effects of any kind, including IO
# 
# - All IO actions must be contained in computation sequences that are
#   clearly separated from the pure functions
# 
# - All sequences that have IO must be called from the main program
# 
#


# Defining a main method makes testing easier
def main(file_path):
    pass

if __name__ == "__main__":
    main(sys.argv[1])
