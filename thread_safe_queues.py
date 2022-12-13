# Using Python's thread-safe queues

# Necessary modules
import argparse
from queue import LifoQueue, PriorityQueue, Queue
import threading
from random import randint
from time import sleep
from itertools import zip_longest

from rich.align import Align
from rich.columns import Columns
from rich.console import Group
from rich.live import Live
from rich.panel import Panel

# Dictionary to map queue names to their respective classes
QUEUE_TYPES = {
    "fifo": Queue,
    "lifo": LifoQueue,
    "heap": PriorityQueue
}

# Defining the products that producers will pick at random and pretend to be working on
PRODUCTS = (
    ":balloon:",
    ":cookie:",
    ":crystal_ball:",
    ":diving_mask:",
    ":flashlight:",
    ":gem:",
    ":gift:",
    ":kite:",
    ":party_popper:",
    ":postal_horn:",
    ":ribbon:",
    ":rocket:",
    ":teddy_bear:",
    ":thread:",
    ":yo-yo:",
)

# The Worker class is the common base class that encapsulates the attributes and behaviors of producer and consumer
class Worker(threading.Thread):
    def __init__(self, speed, buffer):
        super().__init__(daemon=True)
        self.speed = speed
        self.buffer = buffer
        self.product = None
        self.working = False
        self.progress = 0

    @property
    # The state() function to check the state of a worker thread
    # The state property returns a string with either the product’s name and the progress of work or a generic message indicating that the worker is currently idle
    def state(self):
        if self.working:
            return f"{self.product} ({self.progress}%)"
        return ":zzz Idle"

    # The simulate_idle() function to stimulate idle time
    #The simulate_idle() method resets the state of a worker thread and goes to sleep for a few randomly chosen seconds
    def simulate_idle(self):
        self.product = None
        self.working = False
        self.progress = 0
        sleep(randint(1,3))
    
    # The simulate_work() function to stimulate work time
    # The simulate_work() picks a random delay in seconds adjusted to the worker’s speed and progresses through the work
    def simulate_work(self):
        self.working = True
        self.progress = 0
        delay = randint(1, 1 + 15 // self.speed)
        for _ in range(100):
            sleep(delay / 100)
            self.progress += 1

class View:
    def __init__(self, buffer, producers, consumers):
        self.buffer = buffer
        self.producers = producers
        self.consumers = consumers

# The main() function is the entry point, which receives the parsed arguments supplied by parse_args()
def main(args):
    buffer = QUEUE_TYPES[args.queue]()

# The parse_args() supplies parsed arguments to main() function
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-q", "--queue", choices=QUEUE_TYPES, default="fifo")
    parser.add_argument("-p", "--producers", type=int, default=3)
    parser.add_argument("-c", "--consumers", type=int, default=2)
    parser.add_argument("-ps", "--producer-speed", type=int, default=1)
    parser.add_argument("-cs", "--consumer-speed", type=int, default=1)
    return parser.parse_args()

if __name__ == "__main__":
    try:
        main(parse_args())
    except KeyboardInterrupt:
        pass
