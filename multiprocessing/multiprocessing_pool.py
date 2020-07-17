#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import os
import argparse
import threading
import multiprocessing
from functools import partial

from urllib.request import urlopen
from multiprocessing import ProcessError, Pool


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


def download_file(url, directory):
    handle = urlopen(url)
    fname = os.path.basename(url)

    file_dir = os.path.abspath(directory) + "/" + fname
    print("File in directory ===== ", file_dir)
    print("{0} is starting".format(threading.currentThread().getName()))

    with open(file_dir, "wb") as f_handler:
        while True:
            chunk = handle.read(1024)
            if not chunk:
                break
            f_handler.write(chunk)

    msg = "{0} has finished downloading {1}!".format(threading.currentThread().getName(), url)
    print(msg)
    return msg


def thread_active_count():
    print("Active threads count: ", threading.activeCount())


def processes(urls, directory, cores, chanksize):
    if cores is None:
        cpu_cores = multiprocessing.cpu_count()
    else:
        cpu_cores = cores

    try:
        thread_active_count()
        with Pool(processes=cpu_cores) as pool:
            thread_active_count()
            download_file_x = partial(download_file, directory=directory)
            pool.map(download_file_x, urls, chunksize=chanksize)
            # pool.imap(download_file_x, urls, chunksize=chanksize)
            # pool.imap_unordered(download_file_x, urls, chunksize=chanksize)
            thread_active_count()

    except ProcessError as error:
        print('Error: Unable to initialize the {0} thread: \n{1}'.format(
            threading.currentThread().getName(),
            error)
        )

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
    parser.add_argument('--chanksize', dest='chanksize', help='Set chanksize', default=1)
    parser.add_argument('--cores', dest='cpu_cores',
                        help='Set cores for work. If None - will use cores count from host',
                        default=None)

    results = parser.parse_args()
    file_dir = results.file_dir
    cores = results.cpu_cores
    chanksize = results.chanksize

    urls = ["http://www.irs.gov/pub/irs-pdf/f1040.pdf",
            "http://www.irs.gov/pub/irs-pdf/f1040a.pdf",
            "http://www.irs.gov/pub/irs-pdf/f1040ez.pdf",
            "http://www.irs.gov/pub/irs-pdf/f1040es.pdf",
            "http://www.irs.gov/pub/irs-pdf/f1040sb.pdf"
            ] * 10

    if not os.path.exists(file_dir):
        os.makedirs(file_dir)

    processes(urls, file_dir, cores, chanksize)

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
