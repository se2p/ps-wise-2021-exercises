#!/usr/bin/env python

#
# The Hollywood Style Description:
#
# - Larger problem is decomposed into entities using some form of
#       abstraction (objects, modules or similar)
#
# - The entities are never called on directly for ACTIONS (No Action -> No change state)
#       - is_ method
#       - getters
#
# - The entities provide interfaces for other entities to be
#  able to register callbacks
#
# - At certain points of the computation, the entities call on the other
#  entities that have registered for callbacks
#
#


def main(path_to_file):
    pass


if __name__ == "__main__":
    main(sys.argv[1])