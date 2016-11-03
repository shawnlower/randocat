import glob
import hashlib
import subprocess
import sys


from gatherer import EntropyGatherer

class SockstatEntropyGatherer(EntropyGatherer):
    """
    Gather pseudo-random entropy by gathering variable run-time information from
    the system. This consists of things like:
    - Network connections, stats, counters, timers (ss -om)
    """

    def __init__(self, queue):
        self.queue = queue
        self.name = self.__class__.__name__


    def _get_sockstat(self):
        """
        Fetch socket statistics
        """

        return subprocess.check_output(['ss', '-eo'])


    def get_bytes(self, k=16):
        try:
            while True:
                self.queue.put(hashlib.sha1(self._get_sockstat()).digest())
        except KeyboardInterrupt:
            print sys.stderr, 'Exiting due to Ctrl-C'
            pass


class ProcEntropyGatherer(EntropyGatherer):
    """
    Gather pseudo-random entropy by gathering variable run-time information from
    the system. This consists of things like:
    - process scheduling statistics
      (see: http://eaglet.rain.com/rick/linux/schedstat/v15/format-15.html)
    For performance reasons, we'll read /proc directly, vs calling via subprocess
    """

    def __init__(self, queue):
        self.queue = queue
        self.name = self.__class__.__name__


    def _proc_schedstat(self):
        """
        Read data from /proc/*/schedstats and return it as text
        """

        files = glob.glob('/proc/*/schedstat')
        text = ''
        for f in files:
            try:
                text += open(f).read()
            except IOError:
                continue

        return text


    def get_bytes(self, k=16):
        try:
            while True:
                self.queue.put(hashlib.sha1(self._proc_schedstat()).digest())
        except KeyboardInterrupt:
            print sys.stderr, 'Exiting due to Ctrl-C'
            pass


