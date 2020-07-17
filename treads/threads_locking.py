#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import time
import os
import argparse
import logging
import threading

from urllib.request import urlopen
from threading import Thread, Lock, ThreadError

logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] (%(ThreadName)-1s) %(message)s',
                    datefmt="%H:%M:%S"
                    )


class Bgcolors:
    def __init__(self):
        self.get = {
            'HEADER': '\033[95m',
            'OKBLUE': '\033[94m',
            'OKGREEN': '\033[92m',
            'WARNING': '\033[93m',
            'FAIL': '\033[91m',
            'ENDC': '\033[0m',
            'BOLD': '\033[1m',
            'UNDERLINE': '\033[4m'
        }


class StartThreads(Thread):
    def __init__(self, name, daemon, url):
        """Initialize the thread"""
        try:
            Thread.__init__(self)
            self.name = name
            self.daemon = daemon
            self.url = url
            self.lock = Lock()
            self.setDaemon(daemon)
            self.start()
        except ThreadError as error:
            print('Error: Unable to initialize the {0} thread: \n{1}'.format(
                threading.currentThread().getName(),
                error)
            )

    def run(self):
        """Run the thread"""
        handle = urlopen(self.url)
        fname = os.path.basename(self.url)

        logging.debug('Waiting for a lock for {0}'.format(self.name))
        self.lock.acquire()

        try:
            with open(fname, "wb") as f_handler:
                while True:
                    chunk = handle.read(1024)
                    if not chunk:
                        break
                    f_handler.write(chunk)
            print("{0} is starting".format(threading.currentThread().getName()))
            msg = "{0} has finished downloading {1}!".format(self.name, self.url)
            print(msg)
        except Exception as error:
            print('Error: Got issue with {0} thread: \n{1}'.format(self.name, error))
        finally:
            logging.debug('Released a lock for {0}'.format(threading.currentThread().getName()))
            self.lock.release()

    @staticmethod
    def enumerate():
        for thread in threading.enumerate():
            print("Thread name is %s." % thread.getName())

    @staticmethod
    def thread_active_count():
        print("Active threads count: ", threading.activeCount())


def threads(urls):
    try:
        print("TIMEOUT_MAX: ", threading.TIMEOUT_MAX)
        for item, url in enumerate(urls):
            thread = StartThreads(name="Thread-{0}".format(item + 1), daemon=True, url=url)

            StartThreads.thread_active_count()

            if thread.daemon:
                thread.join(timeout=1)

        print("Threading is done")
    except ThreadError as error:
        print("Error: Unable to start thread: \n{0}".format(error))

    return threads


def main():
    start__time = time.time()

    parser = argparse.ArgumentParser(prog='python3 script_name.py -h',
                                     usage='python3 script_name.py {ARGS}',
                                     add_help=True,
                                     prefix_chars='--/',
                                     epilog='''created by Vitalii Natarov''')
    parser.add_argument('--version', action='version', version='v0.1.0')

    urls = [
        # "https://www.irs.gov/pub/irs-pdf/p3.pdf",
        # "https://www.irs.gov/pub/irs-pdf/p15.pdf",
        # "https://www.irs.gov/pub/irs-pdf/p15a.pdf",
        # "https://www.irs.gov/pub/irs-pdf/p15b.pdf",
        # "https://www.irs.gov/pub/irs-pdf/p15t.pdf",
        "http://www.irs.gov/pub/irs-pdf/f1040.pdf",
        "http://www.irs.gov/pub/irs-pdf/f1040a.pdf",
        "http://www.irs.gov/pub/irs-pdf/f1040ez.pdf",
        "http://www.irs.gov/pub/irs-pdf/f1040es.pdf",
        "http://www.irs.gov/pub/irs-pdf/f1040sb.pdf"
    ]

    threads(urls)

    end__time = round(time.time() - start__time, 2)
    print("--- %s seconds ---" % end__time)

    print(
        Bgcolors().get['OKGREEN'], "============================================================",
        Bgcolors().get['ENDC'])
    print(
        Bgcolors().get['OKGREEN'], "==========================FINISHED==========================",
        Bgcolors().get['ENDC'])
    print(
        Bgcolors().get['OKGREEN'], "============================================================",
        Bgcolors().get['ENDC'])


if __name__ == '__main__':
    main()
