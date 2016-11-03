#!/usr/bin/python
#
# implement /dev/random in python
#

import argparse
import logging
import os
import sys
import multiprocessing

import gather_funcs

# Global logger
if '-d' in sys.argv:
    log_level = logging.DEBUG
else:
    log_level = logging.WARNING

logger = logging.basicConfig(level = log_level)

def main(args):
    # Create a queue where we will receive our random data
    q = multiprocessing.Queue()

    # Get a list of entropy gatherers
    gather_modules = []
    for m in filter(lambda x: callable(x), gather_funcs.__dict__.values()):
        gather_modules.append(m(q))

    logging.info("Loaded %s entropy modules [%s]" % (len(gather_modules), ', '.join([
        m.name for m in gather_modules])))

    # Start a process per entropy gatherer
    for m in gather_modules:
        p = multiprocessing.Process(target=m.get_bytes)
        p.daemon = True
        p.start()

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
