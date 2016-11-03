#!/usr/bin/python
#
# implement /dev/random in python
#

import argparse
import logging
import os
import Queue
import sys
import threading

import gather_funcs

# Global logger
if '-d' in sys.argv:
    log_level = logging.DEBUG
else:
    log_level = logging.WARNING

logger = logging.basicConfig(level = log_level)

def main(args):
    # Get a list of entropy gatherers
    gather_modules = filter(lambda x: callable(x), gather_funcs.__dict__.values())
    logging.info("Loaded %s entropy modules [%s]" % (len(gather_modules), ', '.join([
        f.__name__ for f in gather_modules])))

    # Create a queue where we will receive our random data
    q = Queue.Queue()

    # Start a thread per entropy gatherer
    for m in gather_modules:
        func = m(q)
        t = threading.Thread(target=func.get_bytes)
        t.daemon = True
        t.start()

    while True:
        try:
            sys.stdout.write(q.get())
        except KeyboardInterrupt:
            break

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='randocat')
    parser.add_argument('--debug', '-d', action='store_true', default=False, 
                        help="Enable debug output") 
    args = parser.parse_args()

    try:
        main(args)
    except IOError:
        # e.g. broken pipe when piping script through less
        #sys.exit(0)
        pass
