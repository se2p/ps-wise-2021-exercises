
# The Quarantine class for this example. It works with functions, so unit accepts a function
#
class TFQuarantine:

    # UNIT
    def __init__(self, func):
        """
        Note that here we wrap a function not a value!
        """
        self._funcs = [func]

    # BIND
    def bind(self, func):
        """
        The function is stored so we can execute all of them later "lazily"
        """
        self._funcs.append(func)
        return self

    # UNWRAP
    def execute(self):

        def guard_callable(v):
            """
            This always return a value, either because v is indeed a value, or because v is returned
            by an "unsafe" function that we quarantined using a high-order function
            """
            return v() if hasattr(v, '__call__') else v

        value = lambda : None

        for func in self._funcs:
            value = func(guard_callable(value))

        # Ensure that the final result is indeed a VALUE
        value = guard_callable(value)

        if value is not None:
            print(str(value).rstrip('\n'))