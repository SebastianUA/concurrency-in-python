#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import os
import argparse
import logging
import threading
import multiprocessing

from urllib.request import urlopen
from multiprocessing import Process, ProcessError, JoinableQueue

# http://onreader.mdl.ru/MasteringConcurrencyInPython/content/Ch06.html

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
    def __init__(self, name, daemon, queue):
        """Initialize the thread"""
        try:
            Process.__init__(self)
            self.name = name
            self.queue = queue
            self.event = multiprocessing.Event()
            self.daemon = daemon
            self.start()
        except ProcessError as error:
            print('Error: Unable to initialize the {0} thread: \n{1}'.format(
                multiprocessing.current_process().name,
                error)
            )

    def run(self):
        """Run the thread"""
        while True:
            # Get the work from the queue and expand the tuple
            directory, link = self.queue.get(timeout=60)

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
                print("{0} is starting".format(multiprocessing.current_process().name))
                msg = "{0} has finished downloading {1}!".format(self.name, link)
                print(msg)
            except Exception as error:
                print('Error: Got issue with {0} thread: \n{1}'.format(self.name, error))
            # finally:
            #     # print(self.event)
            #     # self.stop()
            #     # self.queue.task_done()

    @staticmethod
    def thread_active_count():
        print("Active threads count: ", threading.activeCount())

    @staticmethod
    def current_process_pid():
        print("Active process count: ", multiprocessing.current_process().pid)


def processes(cores, file_dir, urls):
    try:
        if cores is None:
            cpu_cores = multiprocessing.cpu_count()
        else:
            cpu_cores = cores

        all_processes = []

        # Create a queue to communicate with the worker threads
        queue = JoinableQueue()

        for item in range(cpu_cores):
            process = StartProcesses(name="Process-{0}".format(item + 1), daemon=True, queue=queue)
            all_processes.append(process)
            print("process: ", process)

            StartProcesses.thread_active_count()

        # Put the tasks into the queue as a tuple
        for url in urls:
            logging.info('Queueing {}'.format(url))
            queue.put((file_dir, url))

        # Causes the main thread to wait for the queue to finish processing all the tasks
        for pr in all_processes:
            pr.join(timeout=1)

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
    parser.add_argument('--cores', dest='cpu_cores',
                        help='Set cores for work. If None - will use cores count from host',
                        default=None)

    results = parser.parse_args()
    file_dir = results.file_dir
    cores = results.cpu_cores

    urls = ["http://www.irs.gov/pub/irs-pdf/f1040.pdf",
            "http://www.irs.gov/pub/irs-pdf/f1040a.pdf",
            "http://www.irs.gov/pub/irs-pdf/f1040ez.pdf",
            "http://www.irs.gov/pub/irs-pdf/f1040es.pdf",
            "http://www.irs.gov/pub/irs-pdf/f1040sb.pdf"
            ] * 10

    if not os.path.exists(file_dir):
        os.makedirs(file_dir)

    processes(cores, file_dir, urls)

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
