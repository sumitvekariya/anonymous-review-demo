from typing import List


class BoundedStack:
    """A fixed-capacity LIFO stack of integers."""

    def __init__(self, capacity: int) -> None:
        if not isinstance(capacity, int) or capacity <= 0:
            raise ValueError("capacity must be a positive integer")
        self._capacity: int = capacity
        self._items: List[int] = []

    def push(self, value: int) -> None:
        if len(self._items) >= self._capacity:
            raise ValueError("stack is at capacity")
        self._items.append(value)

    def pop(self) -> int:
        if not self._items:
            raise IndexError("pop from empty stack")
        return self._items.pop()

    def peek(self) -> int:
        if not self._items:
            raise IndexError("peek from empty stack")
        return self._items[-1]

    def size(self) -> int:
        return len(self._items)

    def capacity(self) -> int:
        return self._capacity
