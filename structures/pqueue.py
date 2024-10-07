"""
Skeleton for COMP3506/7505 A2, S2, 2024
The University of Queensland
Joel Mackenzie and Vladimir Morozov
"""

from typing import Any
from structures.entry import Entry
from structures.dynamic_array import DynamicArray

class PriorityQueue:
    """
    An implementation of the PriorityQueue ADT. We have used the implicit
    tree method: an array stores the data, and we use the heap shape property
    to directly index children/parents.

    The provided methods consume keys and values. Keys are called "priorities"
    and should be comparable numeric values; smaller numbers have higher
    priorities.
    Values are called "data" and store the payload data of interest.
    We use the Entry types to store (k, v) pairs.
    """
    
    def __init__(self):
        """
        Empty construction
        """
        self._arr = DynamicArray()
        self._max_priority = 0

    def _parent(self, ix: int) -> int:
        """
        Given index ix, return the index of the parent
        """
        return (ix) // 2

    def insert(self, priority: int, data: Any) -> None:
        """
        Insert some data to the queue with a given priority.
        """
        new = Entry(priority, data)
        # Put it at the back of the heap
        self._arr.append(new)
        ix = self._arr.get_size() - 1
        # Now swap it upwards with its parent until heap order is restored
        while ix > 0:
            parent_ix = self._parent(ix)
            if self._arr[ix].get_key() < self._arr[parent_ix].get_key():
                # Swap if the new entry has higher priority (lower key value)
                self._arr[ix], self._arr[parent_ix] = self._arr[parent_ix], self._arr[ix]
                ix = parent_ix
            elif self._arr[ix].get_key() == self._arr[parent_ix].get_key():
                # If priorities are equal, maintain FIFO order by not swapping
                break
            else:
                # If the new entry has lower priority, stop here
                break
    
        #update max priority if incoming priority is the maximum
        if priority > self._max_priority:
            self._max_priority = priority

    def insert_fifo(self, data: Any) -> None:
        """
        Insert some data to the queue in FIFO mode. Note that a user
        should never mix `insert` and `insert_fifo` calls, and we assume
        that nobody is silly enough to do this (we do not test this).
        """
        self.insert(self._max_priority, data)
        self._max_priority += 1

    def get_min_priority(self) -> Any:
        """
        Return the priority of the min element
        """
        if self.is_empty():
            return None
        return self._arr[0].get_key()

    def get_min_value(self) -> Any:
        """
        Return the highest priority value from the queue, but do not remove it
        """
        if self.is_empty():
            return None
        return self._arr[0].get_value()

    def remove_min(self) -> Any:
        """
        Extract (remove) the highest priority value from the queue.
        You must then maintain the queue to ensure priority order.
        """
        if self.is_empty():
            return None
        
        result = self._arr[0].get_value()
        last_item = self._arr[self.get_size() - 1]
        self._arr.remove_at(self.get_size() - 1)

        if not self.is_empty():
            self._arr[0] = last_item
            self._heapify(0, self.get_size())

        return result

    def get_size(self) -> int:
        """
        Does what it says on the tin
        """
        return self._arr.get_size()

    def is_empty(self) -> bool:
        """
        Ditto above
        """
        return self._arr.is_empty()

    def ip_build(self, input_list: DynamicArray) -> None:
        """
        Take ownership of the list of Entry types, and build a heap
        in-place. That is, turn input_list into a heap, and store it
        inside the self._arr as a DynamicArray. You might like to
        use the DynamicArray build_from_list function. You must use
        only O(1) extra space.
        """
        self._arr = input_list

        start = (self._arr.get_size() // 2) - 1

        # Perform sift-down from the last non-leaf node to the root
        for i in range(start, -1, -1):
            self._heapify(i, self._arr.get_size())

        # Update max_priority
        for i in range(self._arr.get_size()):
            if self._arr[i]:
                self._max_priority = max(self._max_priority, self._arr[i].get_key())

    def sort(self) -> DynamicArray:
        """
        Use HEAPSORT to sort the heap being maintained in self._arr, using
        self._arr to store the output (in-place). You must use only O(1)
        extra space. Once sorted, return self._arr (the DynamicArray of
        Entry types).

        Once this sort function is called, the heap can be considered as
        destroyed and will not be used again (hence returning the underlying
        array back to the caller).
        """
        n = self.get_size()

        for i in range(n // 2 - 1, -1, -1):
            self._heapify(i, n)

        for i in range(n - 1, 0, -1):
            # Move current root to the end
            self._arr[0], self._arr[i] = self._arr[i], self._arr[0]

            self._heapify(0, i)

        return self._arr
    
    def get_arrary(self) -> DynamicArray:
        result = []
        size = self._arr.get_size()
        for i in range(size):
            result.append(self._arr[i])

        return result
    
    def _heapify(self, root: int, size: int) -> None:
        """
        Helper method to restore the min heap property in a subtree.
        """
        smallest = root
        left = 2 * root + 1
        right = 2 * root + 2

        if left < size and self._arr[left].get_key() < self._arr[smallest].get_key():
            smallest = left

        if right < size and self._arr[right].get_key() < self._arr[smallest].get_key():
            smallest = right

        if smallest != root:
            self._arr[root], self._arr[smallest] = self._arr[smallest], self._arr[root]
            self._heapify(smallest, size)
