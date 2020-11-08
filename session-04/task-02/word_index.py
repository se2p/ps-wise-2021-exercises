#!/usr/bin/env python

#
# The Bulletin Board Style Description:
#
# - Larger problem is decomposed into entities using some form of abstraction
#   (objects, modules or similar)
# 
# - The entities are never called on directly for actions
# 
# - Existence of an infrastructure for publishing and subscribing to
#   events, aka the bulletin board
# 
# - Entities post event subscriptions (aka 'wanted') to the bulletin
#   board and publish events (aka 'offered') to the bulletin board. the
#   bulletin board does all the event management and distribution#
#


def main(path_to_file):
    pass


if __name__ == "__main__":
    main(sys.argv[1])