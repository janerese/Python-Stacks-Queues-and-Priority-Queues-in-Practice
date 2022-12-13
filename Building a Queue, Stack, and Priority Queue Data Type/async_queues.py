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

async def main(args):
    session = aiohttp.ClientSession()
    try:
        links = Counter()
        display(links)
    finally:
        await session.close()

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("url")
    parser.add_argument("-d", "--max-depth", type=int, default=2)
    parser.add_argument("-w", "--num-workers", type=int, default=3)
    return parser.parse_args

def display(links):
    for url, count in links.most_common():
        print(f"{count:>3} {url}")

if __name__ == "__main__":
    asyncio.run(main(parse_args()))