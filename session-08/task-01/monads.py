

#
# The One Abstraction, a.k.a, the Identity Monad
#
class TheOne:

    # UNIT
    def __init__(self, v):
        """
        Wrap the value inside the monad, i.e., abstract the value
        """
        self._value = v

    # BIND
    def bind(self, func):
        """
        Apply the given function to the current status of the monad
        """
        self._value = func(self._value)
        return self

    def print_me(self):
        if self._value is not None:
            print(self._value)
