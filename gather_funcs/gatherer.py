
class EntropyGatherer:
    def __init__(self, queue):
        self.queue = queue
        self.name = self.__class__.__name__

    def get_bytes(self, k):
        """
        Returns k bytes of random data
        """
        return Exception("Not implemented.")

    def get_bits(self, k):
        """
        Return k bits of random data
        """
        return Exception("Not implemented.")
