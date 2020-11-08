#!/usr/bin/env python

# Monolithic Style Description:
#
#  - No abstractions
#  - No use of library functions (Let's start with no USER-DEFINED)
#

# Global Constants:
#   Q1: Can those be considered as abstractions? Of which type?
#   Q2: Do they violate the style?
LINES_PER_PAGE = 45
MAX_SIZE_LINE = 80
STOP_FREQUENCY_LIMIT = 100


# Q3: Defining the main method ease testing, but does this count as violation of
# the style?
def main(file_path):
    pass


if __name__ == "__main__":
    main(sys.argv[1])