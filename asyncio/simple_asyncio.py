#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import os
import argparse
import logging
import asyncio
import aiohttp

from functools import partial

logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] %(asctime)s - (%(processName)-1s) - %(name)s - %(message)s '
                           '[in %(funcName)s: %(pathname)s:%(lineno)d]',
                    datefmt="%H:%M:%S"
                    )
logger = logging.getLogger(__name__)


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


async def dir_check(directory):
    print('Check if the dir is present, else - create it')
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
            logger.info("The {0} has been created".format(directory))
    except OSError as err:
        logger.error("Directory {0} can not be created: \n{1}".format(directory, err))

    return directory


async def download_file(session, url, directory):
    async with session.get(url) as response:
        fname = os.path.basename(url)
        file_dir = os.path.abspath(directory) + "/" + fname
        logger.info("File in directory ===== {}".format(file_dir))

        with open(file_dir, "wb") as f_handler:
            logger.info("{0} is starting".format(fname))
            while True:
                # await pauses execution until the 1024 (or less) bytes are read from the stream
                chunk = await response.content.read(1024)
                if not chunk:
                    # We are done reading the file, break out of the while loop
                    break
                f_handler.write(chunk)
    logger.info("{0} has finished downloading {1}!".format(fname, url))

    return download_file


async def fetch(session, url):
    async with session.get(url, raise_for_status=False) as resp:
        # assert resp.status == 200
        print(resp.status, url)
        return resp.status, url


async def main():
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

    urls = [
            "http://www.irs.gov/pub/irs-pdf/f1040.pdf",
            "https://www.irs.gov/pub/irs-prior/f1040a--2015.pdf",
            "https://www.irs.gov/pub/irs-prior/i1040ez--2017.pdf",
            "http://www.irs.gov/pub/irs-pdf/f1040es.pdf",
            "http://www.irs.gov/pub/irs-pdf/f1040sb.pdf"
            ] * 1

    urls_list = []
    async with aiohttp.ClientSession(raise_for_status=True) as session:
        for url in urls:
            # urls_list.append(partial(fetch, session=session, url=url))
            urls_list.append(partial(download_file, session=session, url=url, directory=file_dir))

        await dir_check(file_dir)
        for f in urls_list:
            await f()

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
    loop = asyncio.get_event_loop()
    loop.set_debug(False)

    try:
        tasks = [
            loop.create_task(main())
        ]

        wait_tasks = asyncio.wait(tasks)
        loop.run_until_complete(wait_tasks)
        # loop.run_until_complete(main())
    except Exception as error:
        logger.error(error)
    finally:
        # Shutdown the loop even if there is an exception
        loop.close()
