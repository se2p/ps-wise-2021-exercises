#!/usr/bin/env python

#
# The Kick-forward Style Description:
#
# Variation of the pipeline style, with the following additional constraints:
# 
# - Each function takes an additional parameter, usually the 
#   last, which is another function
# 
# - That function parameter is applied at the end of the current
#   function
# 
# - That function parameter is given as input what would be the
#   output of the current function
# 
# - Larger problem is solved as a pipeline of functions, but where
#   the next function to be applied is given as parameter to the current function
#

# Defining a main method makes testing easier
def main(file_path):
    pass

if __name__ == "__main__":
    main(sys.argv[1])
