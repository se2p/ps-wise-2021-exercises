#!/usr/bin/env python

#
# The Aspects Style Description:
#
# - The problem is decomposed using some form of abstraction (procedures, functions, objects, etc.)
#
# - Aspects of the problem are added to the main program without any
#   edits to the source code of the abstractions. These side functions
#   latch on the main abstractions by naming them, as in "I'm an aspect
#   of foo (even though foo may not know it!)"
#
#

# Defining a main method makes testing easier
def main(file_path):
    pass

if __name__ == "__main__":
    main(sys.argv[1])
