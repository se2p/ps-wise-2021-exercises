from threading import Thread
from queue import Queue


class TheActor(Thread):

    # Note this is NOT the same implementation that you find in the book.
    def __init__(self):
        Thread.__init__(self)
        self.name = str(type(self))
        self.queue = Queue()
        self._stopMe = False

        self.start()

    def run(self):
        # NOTE THAT THIS IS SLIGHTLY DIFFERENT FROM THE BOOK
        while not self._stopMe:
            # Question: How to debug a multi-threaded app?
            # print(self.name + " CHECKING FOR NEW MESSAGES", file=sys.stderr)
            message = self.queue.get()
            # print( self.name + " GOT NEW MESSAGE ", message, file=sys.stderr)

            # NOTE THAT THIS IS SLIGHTLY DIFFERENT FROM THE BOOK
            if message[0] == 'die':
                # Debug
                # print(self.name, "I DIE!")
                self._stopMe = True
            else:
                try:
                    # This might be raised in case messages are not understood
                    self._dispatch(message)
                except Exception as e:
                    print(self.name, "ERROR", e)
                    # QUESTION: Shall we raise an error and die?
                    self._stopMe


# Q: Should this belong to the TheActor instead
def send_message(receiver, message):
    receiver.queue.put(message)
