from time import monotonic
from collections import deque

class Node:
    def __init__(
        self,
        val=None,
        parent=None,
        child=None
    ):
        self.val, self.parent, self.child = val, parent, child

class Deque:
    def __init__(self):
        self.head = Node()
        self.tail = Node()

        self.head.child = self.tail
        self.tail.parent = self.head

    def append(self, val):
        node = Node(
            val=val,
            parent=self.tail.parent,
            child=self.tail
        )
        node.parent.child = node
        self.tail.parent = node

    def appendleft(self, val):
        node = Node(
            val=val,
            parent=self.head,
            child=self.head.child
        )
        node.child.parent = node
        self.head.child = node

    def pop(self):
        cur = self.tail.parent
        if cur is self.head:
            return None
        val = cur.val
        cur.parent.child = self.tail
        self.tail.parent = cur.parent
        del cur
        return val

    def popleft(self):
        cur = self.head.child
        if cur is self.tail:
            return None
        val = cur.val
        cur.child.parent = self.head
        self.head.child = cur.child
        del cur
        return val

    def __iter__(self):
        node = self.head.child
        while node is not self.tail:
            yield node.val
            node = node.child

class FakeDeque:
    def __init__(self):
        self.data = []

    def append(self, val):
        self.data.append(val)

    def appendleft(self, val):
        self.data.insert(0, val)

    def pop(self):
        return self.data.pop()

    def popleft(self):
        return self.data.pop(0)

    def __iter__(self):
        for d in self.data:
            yield d

T = 100 # simulation loops
M = 100 # queue size

for q in [Deque(), FakeDeque(), deque((), M)]:
    start_time = monotonic()
    for simulation in range(T):
        for i in range(M):
            q.append(i)
        for i in range(M):
            q.popleft()
    print(monotonic() - start_time)

# conclusion fake is always faster than linked list in both directions
# deque is surely the fastest
# deque does not have appendleft()
