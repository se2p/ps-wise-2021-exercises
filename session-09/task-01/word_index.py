#!/usr/bin/env python

#
# The Actors Style Description:
#
# Similar to the letterbox style, but where the 'things' have
# independent threads of execution.
# 
# - The larger problem is decomposed into 'things' that make sense for
#   the problem domain 
# 
# - Each 'thing' has a queue meant for other \textit{things} to place
#   messages in it
# 
# - Each 'thing' is a capsule of data that exposes only its
#   ability to receive messages via the queue
# 
# - Each 'thing' has its own thread of execution independent of the
#   others.
#


# Defining a main method makes testing easier
def main(file_path):
    pass

if __name__ == "__main__":
    main(sys.argv[1])
