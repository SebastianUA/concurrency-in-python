#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import os
import argparse
import logging
import threading

from urllib.request import urlopen
from threading import Thread, ThreadError
from queue import Queue

logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] (%(threadName)-1s) %(message)s',
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
    def __init__(self, name, daemon, queue):
        """Initialize the thread"""
        try:
            Thread.__init__(self)
            self.name = name
            self.daemon = daemon
            self.queue = queue
            self.setDaemon(daemon)
            self.start()
        except ThreadError as error:
            print('Error: Unable to initialize the {0} thread: \n{1}'.format(
                threading.currentThread().getName(),
                error)
            )

    def run(self):
        """Run the thread"""
        while True:
            # Get the work from the queue and expand the tuple
            directory, link = self.queue.get()
            try:
                fname = os.path.basename(link)
                handle = urlopen(link)

                file_dir = os.path.abspath(directory) + "/" + fname
                print("File in directory ===== ", file_dir)

                with open(file_dir, "wb") as f_handler:
                    while True:
                        chunk = handle.read(1024)
                        if not chunk:
                            break
                        f_handler.write(chunk)
                print("{0} is starting".format(threading.currentThread().getName()))
                msg = "{0} has finished downloading {1}!".format(self.name, link)
                print(msg)
            except Exception as error:
                print('Error: Got issue with {0} thread: \n{1}'.format(self.name, error))
            finally:
                self.queue.task_done()

    @staticmethod
    def thread_active_count():
        print("Active threads count: ", threading.activeCount())


def workers(urls, thread_counts):
    file_dir = "dir"
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)

    try:
        # Create a queue to communicate with the worker threads
        queue = Queue()
        # Create (thread_counts) worker threads
        for item in range(thread_counts):
            StartThreads(name="Thread-{0}".format(item + 1), daemon=True, queue=queue)

            StartThreads.thread_active_count()

        # Put the tasks into the queue as a tuple
        for url in urls:
            logging.info('Queueing {}'.format(url))
            queue.put((file_dir, url))
        # Causes the main thread to wait for the queue to finish processing all the tasks
        queue.join()

        # print("queue.empty() ------: ", queue.empty())
        # StartThreads.thread_active_count()

        print("Threading is done")
    except ThreadError as error:
        print("Error: Unable to start thread: \n{0}".format(error))

    return workers


def main():
    start__time = time.time()

    parser = argparse.ArgumentParser(prog='python3 script_name.py -h',
                                     usage='python3 script_name.py {ARGS}',
                                     add_help=True,
                                     prefix_chars='--/',
                                     epilog='''created by Vitalii Natarov''')
    parser.add_argument('--version', action='version', version='v0.1.0')
    parser.add_argument('--threads', dest='thread_counts', help='Set thread counts', default=10)

    results = parser.parse_args()
    thread_counts = results.thread_counts

    urls = [
        "https://www.irs.gov/pub/irs-pdf/p3.pdf",
        "https://www.irs.gov/pub/irs-pdf/p15.pdf",
        "https://www.irs.gov/pub/irs-pdf/p15a.pdf",
        "https://www.irs.gov/pub/irs-pdf/p15b.pdf",
        "https://www.irs.gov/pub/irs-pdf/p15t.pdf",
        "http://www.irs.gov/pub/irs-pdf/f1040.pdf",
        "http://www.irs.gov/pub/irs-pdf/f1040a.pdf",
        "http://www.irs.gov/pub/irs-pdf/f1040ez.pdf",
        "http://www.irs.gov/pub/irs-pdf/f1040es.pdf",
        "http://www.irs.gov/pub/irs-pdf/f1040sb.pdf"
    ]

    workers(urls, thread_counts)

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
