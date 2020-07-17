#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# https://stackoverrun.com/ru/q/10677872

import os
import time
import argparse
import threading

from urllib.request import urlopen
from concurrent.futures.thread import ThreadPoolExecutor
from concurrent.futures import as_completed
from concurrent.futures.process import BrokenProcessPool


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
    print('[{0}] is starting.....'.format(threading.current_thread().name))

    handle = urlopen(url)
    fname = os.path.basename(url)

    file_dir = os.path.abspath(directory) + "/" + fname
    print("File in directory ===== ", file_dir)

    try:
        with open(file_dir, "wb") as f_handler:
            while True:
                chunk = handle.read(1024)
                if not chunk:
                    break
                f_handler.write(chunk)
            return "The {0} has been downloaded!".format(fname)
    except Exception as error:
        print("Woops: {0}".format(error))
        return "Woops: {0}".format(error)


def threads_pool_executing(workers_count, file_dir, urls):
    print('[{0}] is starting.....'.format(threading.current_thread().name))
    try:
        with ThreadPoolExecutor(max_workers=workers_count, thread_name_prefix='thread') as ex:
            # future_to_url = {ex.submit(download_file, url, file_dir) for url in urls}
            # future_to_url = ex.map(download_file, url, file_dir) for url in urls
            future_to_url = dict((ex.submit(download_file, url, file_dir), url)
                                 for url in urls)

            try:
                for future in as_completed(future_to_url):
                    url = future_to_url[future]
                    if future.exception() is not None:
                        print('%r generated an exception: %s' % (url,
                                                                 future.exception()))
                    else:
                        print('%r page is %d bytes' % (url, len(future.result())))
            except BrokenProcessPool as error:
                print('could not start new tasks: {}'.format(error))
    except Exception as error:
        print("Woops: {0}".format(error))

    return threads_pool_executing


def main():
    start__time = time.time()

    parser = argparse.ArgumentParser(prog='python3 script_name.py -h',
                                     usage='python3 script_name.py {ARGS}',
                                     add_help=True,
                                     prefix_chars='--/',
                                     epilog='''created by Vitalii Natarov''')
    parser.add_argument('--version', action='version', version='v0.1.0')
    parser.add_argument('--workers', dest='workers_counts', help='Set workers counts for pool executing', default=10)

    results = parser.parse_args()
    workers_counts = results.workers_counts

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
    ] * 100

    file_dir = "dir"
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)

    threads_pool_executing(workers_counts, file_dir, urls)

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
