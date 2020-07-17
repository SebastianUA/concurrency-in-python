#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import os
import argparse
import logging
import threading
import multiprocessing

from urllib.request import urlopen
from multiprocessing import Process, ProcessError, Lock

logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] (%(processName)-1s) %(message)s',
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


class StartProcesses(Process):
    def __init__(self, name, daemon, directory, url):
        """Initialize the thread"""
        try:
            Process.__init__(self)
            self.name = name
            self.directory = directory
            self.url = url
            self.daemon = daemon
            self.lock = Lock()
            self.start()
        except ProcessError as error:
            print('Error: Unable to initialize the {0} thread: \n{1}'.format(
                multiprocessing.current_process().name,
                error)
            )

    def run(self):
        """Run the thread"""
        handle = urlopen(self.url)
        fname = os.path.basename(self.url)

        file_dir = os.path.abspath(self.directory) + "/" + fname
        print("File in directory ===== ", file_dir)

        logging.debug('Waiting for a lock for {0}'.format(self.name))
        self.lock.acquire()

        try:
            with open(file_dir, "wb") as f_handler:
                while True:
                    chunk = handle.read(1024)
                    if not chunk:
                        break
                    f_handler.write(chunk)
            print("{0} is starting".format(self.name))
            msg = "{0} has finished downloading {1}!".format(self.name, self.url)
            print(msg)
        except Exception as error:
            print('Error: Got issue with {0} thread: \n{1}'.format(self.name, error))
        finally:
            logging.debug('Released a lock for {0}'.format(multiprocessing.current_process().name))
            self.lock.release()

    @staticmethod
    def thread_active_count():
        print("Active threads count: ", threading.activeCount())

    @staticmethod
    def current_process_pid():
        print("Active process count: ", multiprocessing.current_process().pid)


def processes(file_dir, urls):
    try:
        for item, url in enumerate(urls):
            process = StartProcesses(name="Process-{0}".format(item + 1), daemon=False, directory=file_dir, url=url)
            print("process: ", process)

            if process.daemon:
                process.join()

            StartProcesses.thread_active_count()

        print("StartProcesses is done")
    except ProcessError as error:
        print("Error: Unable to start a process: \n{0}".format(error))

    return processes


def main():
    start__time = time.time()

    parser = argparse.ArgumentParser(prog='python3 script_name.py -h',
                                     usage='python3 script_name.py {ARGS}',
                                     add_help=True,
                                     prefix_chars='--/',
                                     epilog='''created by Vitalii Natarov''')
    parser.add_argument('--version', action='version', version='v0.1.0')
    parser.add_argument('--dir', dest='file_dir', help='Set directory for files', default="dir")

    results = parser.parse_args()
    file_dir = results.file_dir

    urls = ["http://www.irs.gov/pub/irs-pdf/f1040.pdf",
            "http://www.irs.gov/pub/irs-pdf/f1040a.pdf",
            "http://www.irs.gov/pub/irs-pdf/f1040ez.pdf",
            "http://www.irs.gov/pub/irs-pdf/f1040es.pdf",
            "http://www.irs.gov/pub/irs-pdf/f1040sb.pdf"
            ] * 1

    if not os.path.exists(file_dir):
        os.makedirs(file_dir)

    processes(file_dir, urls)

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
