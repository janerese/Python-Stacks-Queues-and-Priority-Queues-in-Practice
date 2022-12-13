# Testing the FIFO Queue by importing it from the local module

from queues import Queue

# Testing 1
fifo = Queue()
fifo.enqueue("1st")
fifo.enqueue("2nd")
fifo.enqueue("3rd")

print("Testing 1:")
print(fifo.dequeue())
print(fifo.dequeue())
print(fifo.dequeue())

# Testing 2
print("\nTesting 2:")
fifo = Queue("1st", "2nd", "3rd")
print("Initial length:",len(fifo))

for element in fifo:
    print(element)

print("Final length:",len(fifo))
