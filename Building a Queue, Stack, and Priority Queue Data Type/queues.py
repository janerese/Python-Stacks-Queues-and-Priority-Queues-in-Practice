# Building a Queue Data Type
from collections import deque # Representing FIFO and LIFO Queues with a Deque

class Queue:
    def __init__(Self):
        self._elements = deque()
    
    def enqueue(self, element):
        self._elements.append(element)

    def dequeue(self):
        return self._elements.popleft()
        
# Building a Stack Data Type

# Building a PriorityQueue Data Type