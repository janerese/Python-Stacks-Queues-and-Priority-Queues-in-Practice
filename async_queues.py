# This is FIFO Queue

# Using Asynchronous Queues
# Writing a rudimentary web crawler which recursively follows links on a specified website up to a given depth level and counts the number of visits per link
# To fetch data asynchronously, the popular aiohttp library will be used
# To parse HTML hyperlinks, beautifulsoup4 will be used
# To install both libraries, type this command:
# $ python -m pip install aiohttp beautifulsoup4

# Necessary modules
import argparse
import asyncio
from collections import Counter

import aiohttp

from urllib.parse import urljoin
from bs4 import BeautifulSoup

import sys
from typing import NamedTuple

class Job(NamedTuple):
    url: str
    depth: int = 1

async def main(args):
    session = aiohttp.ClientSession()
    try:
        links = Counter()
        queue = asyncio.Queue() # Instantiates an asynchronous FIFO queue
        # Create a number of worker coroutines wrapped in asynchronous tasks that start running as soon as possible in the background on the event loop
        tasks = [
            asyncio.create_task(
                worker(
                    f"Worker-{i + 1}",
                    session,
                    queue,
                    links,
                    args.max_depth,
                )
            )
            for i in range(args.num_workers)
        ]

        await queue.put(Job(args.url)) # Puts the first job in the queue, which kicks off the crawling
        await queue.join() # Causes the main coroutine to wait until the queue has been drained and there are no more jobs to perform

        # Do a graceful cleanup when the background tasks are no longer needed
        for task in tasks:
            task.cancel()
        
        await asyncio.gather(*tasks, return_exceptions=True)

        display(links)
    finally:
        await session.close()

async def worker(worker_id, session, queue, links, max_depth):
    print(f"[{worker_id} starting]", file=sys.stderr)
    while True:
        url, depth = await queue.get()
        links[url] +=1
        try:
            if depth <= max_depth:
                print(f"[{worker_id} {depth=} {url=}]", file=sys.stderr)
                if html := await fetch_html(session, url):
                    for link_url in parse_links(url, html):
                        await queue.put(Job(link_url, depth + 1))
        except aiohttp.ClientError:
            print(f"[{worker_id} failed at {url=}]", file=sys.stderr)

        finally:
            queue.task_done()

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("url")
    parser.add_argument("-d", "--max-depth", type=int, default=2)
    parser.add_argument("-w", "--num-workers", type=int, default=3)
    return parser.parse_args()

def display(links):
    for url, count in links.most_common():
        print(f"{count:>3} {url}")

async def fetch_html(session, url):
    async with session.get(url) as response:
        if response.ok and response.content_type == "text/html":
            return await response.text()

def parse_links(url, html):
    soup = BeautifulSoup(html, features="html.parser")
    for anchor in soup.select("a[href]"):
        href = anchor.get("href").lower()
        if not href.startswith("javascript:"):
            yield urljoin(url,href)

if __name__ == "__main__":
    asyncio.run(main(parse_args()))

