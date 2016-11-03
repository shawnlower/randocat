import sys

from gatherer import EntropyGatherer

BUF_SIZE=16

class RandomEntropyGatherer(EntropyGatherer):
    def __init__(self, queue):
        self.queue = queue
        self.file = open('/dev/random', 'r')
        self.name = self.__class__.__name__

    def get_bytes(self, k=16):
        while True:
            self.queue.put(self.file.read(BUF_SIZE))

class UrandomEntropyGatherer(EntropyGatherer):
    def __init__(self, queue):
        self.queue = queue
        self.file = open('/dev/urandom', 'r')
        self.name = self.__class__.__name__

    def get_bytes(self, k=16):
        while True:
            self.queue.put(self.file.read(BUF_SIZE))

