#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import os
import argparse
import asyncio
import urllib.request


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


def dir_check(directory):
    print('Check if the dir is present, else - create it')
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print("The {0} has been created".format(directory))
    except OSError as err:
        print("Directory {0} can not be created: \n{1}".format(directory, err))

    return directory


async def download_coroutine(url, directory):
    request = urllib.request.urlopen(url)

    filename = os.path.basename(url)
    file_dir = os.path.abspath(directory) + "/" + filename

    with open(file_dir, 'wb') as file_handle:
        while True:
            chunk = request.read(1024)
            if not chunk:
                break
            file_handle.write(chunk)
    msg = 'Finished downloading {filename}'.format(filename=filename)
    return msg


async def main(links):
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

    dir_check(file_dir)

    coroutines = [download_coroutine(url=url, directory=file_dir) for url in links]
    completed, pending = await asyncio.wait(coroutines)
    for item in completed:
        print(item.result())

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
    urls = [
               "http://www.irs.gov/pub/irs-pdf/f1040.pdf",
               "https://www.irs.gov/pub/irs-prior/f1040a--2015.pdf",
               "https://www.irs.gov/pub/irs-prior/i1040ez--2017.pdf",
               "http://www.irs.gov/pub/irs-pdf/f1040es.pdf",
               "http://www.irs.gov/pub/irs-pdf/f1040sb.pdf"
           ] * 1

    event_loop = asyncio.get_event_loop()
    try:
        event_loop.run_until_complete(main(urls))
        # fun1 = asyncio.gather(*[fun("group 1.{}".format(i)) for i in range(1, 6)])
        # fun2 = asyncio.gather(*[fun("group 2.{}".format(i)) for i in range(1, 4)])
        # fun3 = asyncio.gather(*[fun("group 3.{}".format(i)) for i in range(1, 10)])
        # all_groups = asyncio.gather(fun1, fun2, fun3)
        # event_loop.run_until_complete(all_groups)
    finally:
        event_loop.close()
