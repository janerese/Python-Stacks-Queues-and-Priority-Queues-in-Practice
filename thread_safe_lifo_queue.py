# This is the same code as thread_safe_queues.py
# To see the output for the LIFO queue or a STACK, run this script with a LIFO queue
# Type this command:
# $ python thread_safe_lifo_queue.py --queue lifo

# Necessary modules
import argparse
from queue import LifoQueue, PriorityQueue, Queue
import threading
from random import randint
from time import sleep
from itertools import zip_longest
from random import choice, randint

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
        return ":zzz: Idle"

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

# The Producer class
class Producer(Worker):
    def __init__(self, speed, buffer, products):
        super().__init__(speed, buffer)
        self.products = products

    # The run() method is where all the magic happens. A producer works in an infinite loop, choosing a random product and simulating some work before putting that product onto the queue, called a buffer. It then goes to sleep for a random period, and when it wakes up again, the process repeats
    def run(self):
        while True:
            self.product = choice(self.products)
            self.simulate_work()
            self.buffer.put(self.product)
            self.simulate_idle

# The Consumer class
# Similar to producer, but even more straightforward
class Consumer(Worker):
      def run(self):
        while True:
            self.product = self.buffer.get() #  The .get() method is blocking by default, which will keep the consumer thread stopped and waiting until there’s at least one product in the queue
            self.simulate_work()
            self.buffer.task_done()
            self.simulate_idle()

# The View class that defines a view that renders the current state of your producers, consumers, and the queue ten times a second
class View:
    def __init__(self, buffer, producers, consumers):
        self.buffer = buffer
        self.producers = producers
        self.consumers = consumers
    
    def animate(self):
        with Live(self.render(), screen=True, refresh_per_second=10) as live:
            while True:
                live.update(self.render())

    def render(self):
        match self.buffer:
            case PriorityQueue():
                title = "Priority Queue"
                products = map(str, reversed(list(self.buffer.queue)))
            case LifoQueue():
                title = "Stack"
                products = list(self.buffer.queue)
            case Queue():
                title = "Queue"
                products = reversed(list(self.buffer.queue))
            case _:
                title = products = ""

        rows = [
            Panel(f"[bold]{title}:[/] {', '.join(products)}", width=82)
        ]
        pairs = zip_longest(self.producers, self.consumers)
        for i, (producer, consumer) in enumerate(pairs, 1):
            left_panel = self.panel(producer, f"Producer {i}")
            right_panel = self.panel(consumer, f"Consumer {i}")
            rows.append(Columns([left_panel, right_panel], width=40))
        return Group(*rows)

    def panel(self, worker, title):
        if worker is None:
            return ""
        padding = " " * int(29 / 100 * worker.progress)
        align = Align(
            padding + worker.state, align="left", vertical="middle"
        )
        return Panel(align, height=5, title=title)

# The main() function is the entry point, which receives the parsed arguments supplied by parse_args()
def main(args):
    buffer = QUEUE_TYPES[args.queue]()
    # Producer Thread
    producers = [
        Producer(args.producer_speed, buffer, PRODUCTS)
        for _ in range(args.producers)
    ]

    # Consumer Thread
    consumers = [
        Consumer(args.consumer_speed, buffer) for _ in range(args.consumers)
    ]

    for producer in producers:
        producer.start()

    for consumer in consumers:
        consumer.start()

    view = View(buffer, producers, consumers)
    view.animate()

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
