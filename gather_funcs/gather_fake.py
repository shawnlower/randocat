from time import sleep
import sys

from gatherer import EntropyGatherer

class FakeEntropyGatherer(EntropyGatherer):
    def get_bytes(self, k=16):
        while True:
            sleep(0.01)
            self.queue.put('a' * k)

class FastFakeEntropyGatherer(EntropyGatherer):
    def get_bytes(self, k=16):
        while True:
            sleep(0.001)
            self.queue.put('b' * k)
